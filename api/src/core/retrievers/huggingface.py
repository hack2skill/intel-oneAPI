"""Wrapper around HuggingFace embedding models."""
from __future__ import annotations


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Extra, Field
from core.retrievers.base import Embeddings

class HuggingFaceEmbeddings(BaseModel, Embeddings):
    """Wrapper around huggingface transformers feature-extraction pipeline."""
    
    emb_pipeline: Any #: :meta private:
    
    model_name_or_path: str = None
    ipex_enabled: Optional[bool] = False
    """Key word arguments to pass to the model."""
    hf_kwargs: Dict[str, Any] = Field(default_factory=dict)
   
    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        super().__init__(**kwargs)
        try:
            from transformers import (
                AutoConfig,
                AutoModel,
                AutoTokenizer,
                pipeline
            )

        except ImportError as exc:
            raise ImportError(
                "Could not import transformers python package. "
                "Please install it with `pip install transformers`."
            ) from exc
        
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name_or_path,
            cache_dir=self.hf_kwargs.get("cache_dir", ".cache"),
            use_fast=True,
            revision=self.hf_kwargs.get("model_revision", None),
            keep_accents=self.hf_kwargs.get("keep_accents", False),
            do_lower_case=self.hf_kwargs.get("do_lower_case", False)
        )
        config = AutoConfig.from_pretrained(
            self.model_name_or_path,
            cache_dir=self.hf_kwargs.get("cache_dir", ".cache"),
            revision=self.hf_kwargs.get("model_revision", None),
        )
        model = AutoModel.from_pretrained(
            self.model_name_or_path,
            from_tf=bool(".ckpt" in self.model_name_or_path),
            config=config,
            cache_dir=self.hf_kwargs.get("cache_dir", ".cache"),
            revision=self.hf_kwargs.get("model_revision", None)
        )

        if self.ipex_enabled:
            try:
                import intel_extension_for_pytorch as ipex
            except:
                assert False, "transformers 4.29.0 requests IPEX version higher or equal to 1.12"
            model = ipex.optimize(model)
        
        self.emb_pipeline = pipeline(
            task="feature-extraction",
            model=model,
            tokenizer=tokenizer
        )

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute doc embeddings using a HuggingFace transformer model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.emb_pipeline(texts, return_tensors = "pt")
        embeddings = [emb[0].numpy().mean(axis=0).tolist() for emb in embeddings]

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a HuggingFace transformer model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        text = text.replace("\n", " ")
        embedding = self.emb_pipeline(text, return_tensors = "pt")[0].numpy().mean(axis=0)
        return embedding.tolist()