"""Wrappers around retrivers modules."""
import logging

from core.retrievers.huggingface import HuggingFaceEmbeddings
from core.retrievers.tfidf import TFIDFEmbeddings

logger = logging.getLogger(__name__)


__all__ = [
    "HuggingFaceEmbeddings",
    "TFIDFEmbeddings"
]

