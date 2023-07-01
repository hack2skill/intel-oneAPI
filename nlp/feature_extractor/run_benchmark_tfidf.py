#!/usr/bin/env python
# coding=utf-8
# Copyright 2023 C5ailabs Team (Authors: Rohit Sroch) All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Run a retriever benchmark (TFIDFEmbeddings) Intel® Extension for Scikit-Learn vs Vanilla Scikit-Learn
"""
import argparse
import os
import timeit
import numpy as np
import webvtt
from glob import glob

from tfidf import TFIDFEmbeddings

def get_size(path):
    """A simple function gets the size from a path"""
    return str(round(os.path.getsize(path)/(1024*1024), 3))

def str_np(iterable):
    """A simple function results printable value"""
    return str(np.median(iterable).round(5)), str(np.std(iterable).round(5))

def get_subtitles_as_docs(course_dir):
    # format of courses folder structure is courses/{topic_name}/Study-Material/{week_name}/{subtopic_name}/subtitle-en.vtt
    path = os.path.join(course_dir, "*/Study-Material/*/*/*.vtt")
    subtitle_fpaths = glob(path)
    
    docs = []
    for subtitle_fpath in subtitle_fpaths:
        subtitles = webvtt.read(subtitle_fpath)
        for index, subtitle in enumerate(subtitles):
            docs.append(subtitle.text)
    
    return docs

def train_tfidf_emb_model(tfidf_emb_model, texts):
    """using .fit_transform"""
    def warmup(inputs):
        for _ in range(100): tfidf_emb_model.embed_documents(
                inputs, is_preprocess=args.is_preprocess)
    # perform warmup before running inference
    warmup([texts[0]])

    def run_train():
        tfidf_emb_model.embed_documents(
            texts, is_preprocess=args.is_preprocess)
        
    output = str_np(timeit.repeat(
        stmt="""run_train()""", number=1, repeat=50, globals=locals()))
    
    benchmark = {"avg_time(sec)": output[0], "std_time(sec)": output[1]}
    
    return benchmark

def infer_tfidf_emb_model(tfidf_emb_model, texts, batch_size=8):
    """using .transform"""

    tfidf_emb_model.embed_documents(texts, is_preprocess=args.is_preprocess)
    num_batches = int(len(texts) / batch_size)
    def warmup(inputs):
        for _ in range(100): tfidf_emb_model.embed_queries(
                inputs, is_preprocess=args.is_preprocess)
    # perform warmup before running inference
    warmup([texts[0]])

    def run_infer():
        for index in range(num_batches):
            batch_texts = texts[index * batch_size: (index + 1) * batch_size]
            #if len(batch_texts) > 0:
            tfidf_emb_model.embed_queries(batch_texts, is_preprocess=args.is_preprocess)
        
    output = str_np(timeit.repeat(
        stmt="""run_infer()""", number=1, repeat=50, globals=locals()))
    
    benchmark = {"avg_time(sec)": output[0], "std_time(sec)": output[1]}
    
    return benchmark


def main(args):
    
    print("*********Enable Intel® Extension for Scikit-Learn: {}*********".format(
        args.intel_scikit_learn_enabled
    ))
    # get the contexts as docs with metadata
    docs = get_subtitles_as_docs(args.course_dir)
    docs = docs[: args.max_samples]
    
    # load tfidf emb model
    tfidf_emb_model = TFIDFEmbeddings(
        intel_scikit_learn_enabled=args.intel_scikit_learn_enabled
    )

    print("*"*100)
    print("*********Training TFIDFVectorizer Benchmark (.fit_transform func)*********")
    benchmark = train_tfidf_emb_model(tfidf_emb_model, docs)
    trainTime = float(benchmark["avg_time(sec)"])
    print("Train time: %.3f ms" % (trainTime * 1000))

    print("*"*100)
    print("*********Inference TFIDFVectorizer Benchmark (.transform func)*********")
    benchmark = infer_tfidf_emb_model(tfidf_emb_model, docs, args.batch_size)
    
    eval_samples = min(args.max_samples, len(docs))
    samples = eval_samples - (eval_samples % args.batch_size) 
    evalTime = float(benchmark["avg_time(sec)"])
    print('Batch size = %d' % args.batch_size)
    print("Latency: %.3f ms" % (evalTime / samples * 1000))
    print("Throughput: {} samples/sec".format(samples / evalTime))



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a retriever benchmark (TFIDFEmbeddings)")
    
    parser.add_argument(
        "--course_dir",
        type=str,
        help="Base directory containing courses",
        required=True
    )
    parser.add_argument(
        "--intel_scikit_learn_enabled",
        action="store_true",
        help="Whether to use intel extension for scikit learn in case of emb_model_type as syntactic",
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        help="Maximum samples considered for benchmark",
        default=300
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        help="Batch size for benchmark",
        default=8
    )
    parser.add_argument(
        "--is_preprocess",
        action="store_true",
        help="Whether to preprocess text",
    )

    args = parser.parse_args()

    main(args)
