#!/usr/bin/env python
# coding=utf-8
# Copyright 2023 C5ailabs Team All rights reserved.
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
Extractive Question Answering for LEAP platform
"""
from transformers import (
    AutoConfig,
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    pipeline
)
# optimum-intel
from optimum.intel import INCModelForQuestionAnswering

# retrievers
from core.retrievers.huggingface import HuggingFaceEmbeddings
from core.retrievers.tfidf import TFIDFEmbeddings
from core.retrievers.faiss_vector_store import FAISS

from abc import ABC, abstractmethod
from pydantic import  Extra, BaseModel
from typing import List, Optional, Dict, Any

from utils.logging_handler import Logger

class BaseQuestionAnswering(BaseModel, ABC):
    """Base Question Answering interface"""

    @abstractmethod
    async def retrieve_docs(
        self,
        question: str,
        top_n: Optional[int] = 2,
        sim_score: Optional[float] = 0.9
    ) -> List[str]:
        """Take in a question and return List of top_n docs"""

    @abstractmethod
    async def span_answer(
        self,
        question: str,
        context: List[str],
        doc_stride: Optional[int] = 128,
        max_answer_len: Optional[int] = 30,
        max_seq_len: Optional[int] = 512,
        top_k: Optional[int] = 1
    ) -> Dict:
        """Take in a question and context and return List of top_k answer as dict."""
    
    @abstractmethod
    async def predict(
        self, 
        question: str,
        doc_stride: Optional[int] = 128,
        max_answer_length: Optional[int] = 30,
        max_seq_length: Optional[int] = 512,
        top_n: Optional[int] = 2,
        top_k: Optional[int] = 1
    ) -> Dict:
        """Predict answer from question and context"""


def load_qa_model(
        model_name_or_path, 
        model_type="vanilla_fp32",
        ipex_enabled=False, 
        model_revision="main", 
        keep_accents=False,
        do_lower_case=False,
        cache_dir=".cache"):
    """load a QA model"""
    qa_pipeline = None

    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        cache_dir=cache_dir,
        use_fast=True,
        revision=model_revision,
        keep_accents=keep_accents,
        do_lower_case=do_lower_case,
    )
    if model_type == "vanilla_fp32":
        config = AutoConfig.from_pretrained(
            model_name_or_path,
            cache_dir=cache_dir,
            revision=model_revision
        )
        model = AutoModelForQuestionAnswering.from_pretrained(
            model_name_or_path,
            from_tf=bool(".ckpt" in model_name_or_path),
            config=config,
            cache_dir=cache_dir,
            revision=model_revision
        )
        if ipex_enabled:
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
    elif model_type == "quantized_int8":

        model = INCModelForQuestionAnswering.from_pretrained(
            model_name_or_path,
            cache_dir=cache_dir,
            revision=model_revision
        )
        qa_pipeline = pipeline(
            task="question-answering",
            model=model,
            tokenizer=tokenizer
        )

    return qa_pipeline

def load_emb_model(
        model_name_or_path,
        tfidf_vocab_path,
        model_type="semantic",
        intel_scikit_learn_enabled=True,
        ipex_enabled=False, 
        model_revision="main", 
        keep_accents=False,
        do_lower_case=False,
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
                "do_lower_case": do_lower_case,
                "cache_dir": cache_dir
            }
        )
    elif model_type == "syntactic":
        emb_model = TFIDFEmbeddings(
            intel_scikit_learn_enabled=intel_scikit_learn_enabled,
            tfidf_kwargs = {
                "tfidf_vocab_path": tfidf_vocab_path
            }
        )
    
    return emb_model

def load_faiss_vector_index(
        faiss_vector_index_path, 
        emb_model,
        normalize_L2=False):
    
    faiss_vector_index = FAISS.load_local(
        faiss_vector_index_path, emb_model, 
        normalize_L2=normalize_L2)

    return faiss_vector_index

class ExtractiveQuestionAnswering(BaseQuestionAnswering):
    """QuestionAnswering wrapper should take in a question and return a answer."""

    emb_model: Any = None
    emb_model_type: Optional[str] = "semantic"

    qa_model: Any = None
    qa_model_type: Optional[str] = "vanilla_fp32"

    faiss_vector_index: Any = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
    
    @classmethod
    def load(cls, 
            emb_model_name_or_path: str, 
            qa_model_name_or_path: str, 
            faiss_vector_index_path: str, 
            **kwargs):
        """
          Args:
            emb_model_path (str): Embedding model path
            qa_model_path (str): Question Answering model path
            faiss_vector_index (str): Faiss Context vector index path
        """

        emb_model_type = kwargs.get("emb_model_type", "semantic")
        qa_model_type = kwargs.get("qa_model_type", "vanilla_fp32")
        normalize_L2 = kwargs.get("normalize_L2", False)

        # load the emb model
        emb_model = load_emb_model(
            emb_model_name_or_path,
            faiss_vector_index_path,
            model_type=emb_model_type,
            intel_scikit_learn_enabled=kwargs.get("intel_scikit_learn_enabled", True),
            ipex_enabled=kwargs.get("ipex_enabled", False), 
            model_revision=kwargs.get("model_revision", "main"), 
            keep_accents=kwargs.get("keep_accents", False),
            do_lower_case=kwargs.get("do_lower_case", False),
            cache_dir=kwargs.get("cache_dir", ".cache")
        )
        # load the qa model
        qa_model = load_qa_model(
            qa_model_name_or_path,
            model_type=qa_model_type,
            ipex_enabled=kwargs.get("ipex_enabled", False), 
            model_revision=kwargs.get("model_revision", "main"), 
            keep_accents=kwargs.get("keep_accents", False),
            do_lower_case=kwargs.get("do_lower_case", False),
            cache_dir=kwargs.get("cache_dir", ".cache")
        )

        # load faiss vector index
        faiss_vector_index = load_faiss_vector_index(
            faiss_vector_index_path,
            emb_model=emb_model,
            normalize_L2=normalize_L2
        )

        return cls(
            emb_model=emb_model, 
            emb_model_type=emb_model_type, 
            qa_model=qa_model, 
            qa_model_type=qa_model_type, 
            faiss_vector_index=faiss_vector_index
        )
    
    async def retrieve_docs(
        self,
        question: str,
        top_n: Optional[int] = 2,
        sim_score: Optional[float] = 0.9
    ) -> List[str]:
        """Take in a question and return List of top_n docs"""
        docs = self.faiss_vector_index.similarity_search(
            question, top_n,
            sim_score=sim_score)
        
        return docs
    
    async def span_answer(
        self,
        question: str,
        context: str,
        doc_stride: Optional[int] = 128,
        max_answer_length: Optional[int] = 30,
        max_seq_length: Optional[int] = 512,
        top_k: Optional[int] = 1
    ) -> Dict:
        """Take in a question and context and return List of top_k answer as dict."""
        
        preds = self.qa_model(
            question=question,
            context=context,
            doc_stride=doc_stride,
            max_answer_len=max_answer_length,
            max_seq_len=max_seq_length,
            top_k=top_k
        )
        return preds
    
    async def predict(
        self, 
        question: str,
        doc_stride: Optional[int] = 128,
        max_answer_length: Optional[int] = 30,
        max_seq_length: Optional[int] = 512,
        top_n: Optional[int] = 2,
        top_k: Optional[int] = 1
    ) -> Dict:
        """Predict answer from question and context"""

        docs = await self.retrieve_docs(question, top_n)
        relevant_contexts = [
            {"context": doc.page_content, "metadata": doc.metadata}
            for doc in docs
        ]

        contexts = [doc.page_content  for doc in docs]
        context = ". ".join(contexts)
        preds = await self.span_answer(
            question, context, doc_stride, 
            max_answer_length, max_seq_length, top_k)
        
        relevant_context_id = -1
        for index, dict_ in enumerate(relevant_contexts):
            if preds["answer"] in dict_["context"]:
                relevant_context_id = index
                break
        
        output = { 
            "question": question,
            "context": context,
            "answer": preds["answer"],
            "score": preds["score"],
            "relevant_context_id": relevant_context_id,
            "relevant_contexts": relevant_contexts
        }

        return output

