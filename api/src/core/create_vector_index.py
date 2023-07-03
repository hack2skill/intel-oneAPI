
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
Create a retriever vector index for faster search during inference using FAISS
"""
import argparse
import os
import sys
sys.path.append(os.getcwd())
import webvtt
from glob import glob

from core.retrievers.huggingface import HuggingFaceEmbeddings
from core.retrievers.tfidf import TFIDFEmbeddings
from core.retrievers.faiss_vector_store import FAISS
from core.retrievers.docstore import Document

def get_subtitles_as_docs(course_dir):
    # format of courses folder structure is courses/{topic_name}/{week_name}/{subtopic_name}/subtitle-en.vtt
    path = os.path.join(course_dir, "*/*/*/*.vtt")
    subtitle_fpaths = glob(path)
    
    docs = []
    for subtitle_fpath in subtitle_fpaths:
        topic_name = subtitle_fpath.split("/")[-4]
        week_name =  subtitle_fpath.split("/")[-3]
        subtopic_name = subtitle_fpath.split("/")[-2]
        file_name = subtitle_fpath.split("/")[-1]

        subtitles = webvtt.read(subtitle_fpath)
        for index, subtitle in enumerate(subtitles):
            docs.append(
                Document(
                    page_content=subtitle.text,
                    metadata={
                        "doc_id": index,
                        "start_timestamp": subtitle.start,
                        "end_timestamp": subtitle.end,
                        "topic_name": topic_name,
                        "week_name": week_name,
                        "subtopic_name": subtopic_name,
                        "file_name": file_name,
                        "fpath": subtitle_fpath
                    })
            )
    
    return docs

def load_emb_model(
        model_name_or_path,
        model_type="semantic",
        intel_scikit_learn_enabled=True,
        ipex_enabled=False, 
        model_revision="main", 
        keep_accents=False,
        cache_dir=".cache"
    ):
    """load a Embedding model"""
    emb_model = None

    if model_type == "semantic":
        emb_model = HuggingFaceEmbeddings(
            model_name_or_path=model_name_or_path,
            ipex_enabled=ipex_enabled,
            hf_kwargs={
                "model_revision": model_revision,
                "keep_accents": keep_accents,
                "cache_dir": cache_dir
            }
        )
    elif model_type == "syntactic":
        emb_model = TFIDFEmbeddings(
            intel_scikit_learn_enabled=intel_scikit_learn_enabled
        )
    
    return emb_model


def main(args):
    
    if args.emb_model_type == "semantic":
        print("**********Creating a Semantic vector index using \
              HuggingFaceEmbeddings with `model_name_or_path`={}**********".format(
                   args.model_name_or_path
              ))
    elif args.emb_model_type == "syntactic":
        print("**********Creating a Syntactic vector index using TFIDFEmbeddings**********")

    # get the contexts as docs with metadata
    docs = get_subtitles_as_docs(args.course_dir)
    # get the embedding model
    emb_model = load_emb_model(
        args.model_name_or_path,
        model_type=args.emb_model_type,
        intel_scikit_learn_enabled=args.intel_scikit_learn_enabled,
        ipex_enabled=args.ipex_enabled, 
        keep_accents=args.keep_accents  
    )

    vector_index = FAISS.from_documents(
        docs, emb_model, normalize_L2=args.normalize_L2)
    save_path = "faiss_emb_index" if args.output_dir is None \
        else os.path.join(args.output_dir, "faiss_emb_index")
    vector_index.save_local(save_path)

    if args.emb_model_type == "syntactic":
        emb_model.save_tfidf_vocab(emb_model.vectorizer.vocabulary_, save_path)

    print("*"*100)
    print("Validating for example query...")
    if args.emb_model_type == "syntactic":
        # reload with tfidf vocab
        emb_model = TFIDFEmbeddings(
            intel_scikit_learn_enabled=args.intel_scikit_learn_enabled,
            tfidf_kwargs = {
                "tfidf_vocab_path": save_path
            }
        )

    vector_index = FAISS.load_local(
        save_path, emb_model, normalize_L2=args.normalize_L2)
    query = "How does a neural network help in predicting housing prices?"
    docs = vector_index.similarity_search(query, k=3)
    print("Relevant Docs: {}".format(docs))

    print("*"*100)
    print("😊 FAISS is a local vector index sucessfully saved with name faiss_emb_index")

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Preprocess course video subtitle (.vtt) file")
    
    parser.add_argument(
        "--course_dir",
        type=str,
        help="Base directory containing courses",
        required=True
    )
    parser.add_argument(
        "--emb_model_type",
        type=str,
        default="syntactic",
        help="Embedding model type as semantic or syntactic",
        choices=["semantic", "syntactic"]
    )
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        default=None,
        help="Hugging face model_name_or_path in case of emb_model_type as semantic"
    )
    parser.add_argument(
        "--keep_accents",
        action="store_true",
        help="To preserve accents (vowel matras / diacritics) while tokenization in case of emb_model_type as semantic",
    )
    parser.add_argument(
        "--intel_scikit_learn_enabled",
        action="store_true",
        help="Whether to use intel extension for scikit learn in case of emb_model_type as syntactic",
    )
    parser.add_argument(
        "--ipex_enabled",
        action="store_true",
        help="Whether to use intel extension for pytorch in case emb_model_type as semantic",
    )
    parser.add_argument(
        "--normalize_L2",
        action="store_true",
        help="Whether to normalize embedding, usually its a good idea in case of emb_model_type as syntactic",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Output dir where index will be saved"
    )

    args = parser.parse_args()

    # sanity checks
    if args.emb_model_type == "semantic":
        if args.model_name_or_path is None:
            raise ValueError("Please provide valid `model_name_or_path` as emb_model_type = `semantic`")
    elif args.emb_model_type == "syntactic":
        if args.model_name_or_path is not None:
            raise ValueError("Please don't provide `model_name_or_path` as emb_model_type = `syntatic`")

    if args.output_dir is not None:
        os.makedirs(args.output_dir, exist_ok=True)

    main(args)