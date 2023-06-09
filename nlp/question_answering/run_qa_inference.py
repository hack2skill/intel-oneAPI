#!/usr/bin/env python
# coding=utf-8
# Copyright 2023 C5ailabs Team (Authors: Rohit Sroch) All rights reserved.
# Copyright 2020 The HuggingFace Team All rights reserved.
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
Inference of a 🤗 Transformers model for question answering.
"""

import argparse
import os

from transformers import (
    AutoConfig,
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    pipeline
)

# optimum-intel
from optimum.intel import INCModelForQuestionAnswering

from transformers.utils import check_min_version

os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Will error if the minimal version of Transformers is not installed. Remove at your own risks.
check_min_version("4.29.0")


def parse_args():
    parser = argparse.ArgumentParser(description="Inference transformers model on a Question Answering task")
    
    ####################################
    # Model Arguments
    ####################################
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to pretrained model or model identifier from huggingface.co/models.",
        required=True,
    )
    parser.add_argument(
        "--max_seq_length",
        type=int,
        default=384,
        help=(
            "The maximum total input sequence length after tokenization. Sequences longer than this will be truncated,"
            " sequences shorter will be padded if `--pad_to_max_lengh` is passed."
        ),
    )
    parser.add_argument(
        "--config_name",
        type=str,
        default=None,
        help="Pretrained config name or path if not the same as model_name",
    )
    parser.add_argument(
        "--tokenizer_name",
        type=str,
        default=None,
        help="Pretrained tokenizer name or path if not the same as model_name",
    )
    parser.add_argument(
        "--keep_accents",
        action="store_true",
        help="To preserve accents (vowel matras / diacritics) while tokenization",
    )
    parser.add_argument(
        "--do_lower_case",
        action="store_true",
        help="Whether to lower case while tokenization",
    )
    parser.add_argument(
        "--cache_dir",
        type=str,
        help="Where do you want to store the pretrained models downloaded from huggingface.co",
        default='.cache'
    )
    parser.add_argument(
        "--model_revision",
        type=str,
        help="The specific model version to use (can be a branch name, tag name or commit id).",
        default='main'
    )
    parser.add_argument(
        "--model_type",
        type=str,
        help="Type of the model, Whether its quantized or vanilla",
        default='vanilla_fp32',
        choices=["vanilla_fp32", "quantized_int8"]
    )
    parser.add_argument(
        "--ipex_enabled", 
        action="store_true", 
        help="Whether to enable IPEX (Intel Extention for Pytorch)"
    )
    ####################################
    # Other Arguments
    ####################################
    parser.add_argument(
        "--doc_stride",
        type=int,
        default=128,
        help="When splitting up a long document into chunks how much stride to take between chunks.",
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=1,
        help="The number of answers to return (will be chosen by order of likelihood).",
    )
    parser.add_argument(
        "--max_answer_length",
        type=int,
        default=30,
        help=(
            "The maximum length of an answer that can be generated. This is needed because the start "
            "and end predictions are not conditioned on one another."
        ),
    )
    
    args = parser.parse_args()

    return args


def load_qa_pipeline(args):
    """load the QA pipeline"""
    qa_pipeline = None

    tokenizer = AutoTokenizer.from_pretrained(
        args.tokenizer_name if args.tokenizer_name else args.model_name_or_path,
        cache_dir=args.cache_dir,
        use_fast=True,
        revision=args.model_revision,
        keep_accents=args.keep_accents,
        do_lower_case=args.do_lower_case
    )
    if args.model_type == "vanilla_fp32":
        config = AutoConfig.from_pretrained(
            args.config_name if args.config_name else args.model_name_or_path,
            cache_dir=args.cache_dir,
            revision=args.model_revision
        )
        model = AutoModelForQuestionAnswering.from_pretrained(
            args.model_name_or_path,
            from_tf=bool(".ckpt" in args.model_name_or_path),
            config=config,
            cache_dir=args.cache_dir,
            revision=args.model_revision
        )
        if args.ipex_enabled:
            try:
                import intel_extension_for_pytorch as ipex
            except:
                assert False, "transformers 4.29.0 requests IPEX version higher or equal to 1.12"
            model = ipex.optimize(model)

        qa_pipeline = pipeline(
            task="question-answering",
            model=model,
            tokenizer=tokenizer
        )
    elif args.model_type == "quantized_int8":

        model = INCModelForQuestionAnswering.from_pretrained(
            args.model_name_or_path,
            cache_dir=args.cache_dir,
            revision=args.model_revision
        )
        qa_pipeline = pipeline(
            task="question-answering",
            model=model,
            tokenizer=tokenizer
        )

    return qa_pipeline



def main():

    args = parse_args()

    qa_pipeline = load_qa_pipeline(args)
    
    print("*"*100)
    context = input("Type Context >>>")
    question = input("Type Question >>>")
    print("*"*100)
    preds = qa_pipeline(
        question=question,
        context=context,
        doc_stride=args.doc_stride,
        max_answer_len=args.max_answer_length,
        max_seq_len=args.max_seq_length,
        top_k=args.top_k
    )
    print(
        f"score: {round(preds['score'], 4)}, start: {preds['start']}, end: {preds['end']}, answer: {preds['answer']}"
    )


if __name__ == "__main__":
    main()