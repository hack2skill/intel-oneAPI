"""Wrapper around sklearn TF-IDF vectorizer"""
from __future__ import annotations

import os
import pickle
from collections import defaultdict

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Extra, Field
from core.retrievers.base import Embeddings

try:
    from nltk.tokenize import word_tokenize
    from nltk import pos_tag
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import wordnet as wn
except ImportError as exc:
    raise ImportError(
        "Could not import nltk python package. "
        "Please install it with `pip install nltk`."
    ) from exc


class TFIDFEmbeddings(BaseModel, Embeddings):
    """Wrapper around sklearn TFIDF vectorizer."""
    
    vectorizer: Any #: :meta private:

    intel_scikit_learn_enabled: Optional[bool] = True
    """Key word arguments to pass to the model."""
    tfidf_kwargs: Dict[str, Any] = Field(default_factory=dict)
   
    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        super().__init__(**kwargs)
        try:
            if self.intel_scikit_learn_enabled:
                # Turn on scikit-learn optimizations with these 2 simple lines:
                from sklearnex import patch_sklearn
                patch_sklearn()

            from sklearn.feature_extraction.text import TfidfVectorizer
        except ImportError as exc:
            raise ImportError(
                "Could not import scikit-learn and scikit-learn-intelex python package. "
                "Please install it with `pip install scikit-learn scikit-learn-intelex`."
            ) from exc
        
        if self.tfidf_kwargs.get("tfidf_vocab_path", None) is not None:
            print("******Loading tfidf_vocab.pkl ********")
            path = os.path.join(self.tfidf_kwargs.get("tfidf_vocab_path"), "tfidf_vocab.pkl")

            with open(path, "rb") as fp:
                tfidf_vocab = pickle.load(fp)
                self.tfidf_kwargs["vocabulary"] = tfidf_vocab
                self.tfidf_kwargs.pop("tfidf_vocab_path")
        
        self.vectorizer = TfidfVectorizer(**self.tfidf_kwargs)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
    
    def save_tfidf_vocab(self, tfidf_vocab, save_path):
        """save the tfidf vectorizer object"""

        path = os.path.join(save_path, "tfidf_vocab.pkl")
        with open(path, "wb") as f:
            pickle.dump(tfidf_vocab, f)

    def embed_documents(self, texts: List[str], is_preprocess: bool=False) -> List[List[float]]:
        """Compute doc embeddings using a HuggingFace transformer model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        if is_preprocess:
            texts = list(map(lambda x: self._preprocess_query(x.replace("\n", " ")), texts))
        else:
            texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.vectorizer.fit_transform(texts)
        embeddings = [emb.toarray().astype("float32")[0].tolist() for emb in embeddings]

        return embeddings

    def embed_query(self, text: str, is_preprocess: bool=False) -> List[float]:
        """Compute query embeddings using a HuggingFace transformer model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        if is_preprocess:
            text = self._preprocess_query(text.replace("\n", " "))
        else:
            text = text.replace("\n", " ")
        embedding = self.vectorizer.fit_transform([text]).toarray().astype("float32")[0]
        return embedding.tolist()
    
    def _preprocess_query(self, query):
        """preprocess the query"""

        # Next change is lower case using apply and lambda function
        query_transformed  = word_tokenize(query)
        # Now to remove stopwords, lemmatisation and stemming
        # We need p.o.s (part of speech) tags to understand if its a noun or a verb
        tag_map = defaultdict(lambda: wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV
        
        _stopwords = stopwords.words('english')
        _query = ""
        # Instantiate the lemmatizer
        word_lem = WordNetLemmatizer()
        for word, tag in pos_tag(query_transformed):
            # Loop over the entry in the text column.
            # If the word is not in the stopword
            if word not in _stopwords and (word.isalpha() or word.isalnum() or word.isnumeric()):
                # Run our lemmatizer on the word.
                word = str(word_lem.lemmatize(word, tag_map[tag[0]]))
                # Now add to final words
                _query += word + " "
       
        return _query.strip()