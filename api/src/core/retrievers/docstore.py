"""Interface to access to place that stores documents."""

from typing import Dict, Union

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Interface for interacting with a document."""

    page_content: str
    metadata: dict = Field(default_factory=dict)

class Docstore(ABC):
    """Interface to access to place that stores documents."""

    @abstractmethod
    def search(self, search: str) -> Union[str, Document]:
        """Search for document.

        If page exists, return the page summary, and a Document object.
        If page does not exist, return similar entries.
        """

class AddableMixin(ABC):
    """Mixin class that supports adding texts."""

    @abstractmethod
    def add(self, texts: Dict[str, Document]) -> None:
        """Add more documents."""

class InMemoryDocstore(Docstore, AddableMixin):
    """Simple in memory docstore in the form of a dict."""

    def __init__(self, _dict: Dict[str, Document]):
        """Initialize with dict."""
        self._dict = _dict

    def add(self, texts: Dict[str, Document]) -> None:
        """Add texts to in memory dictionary."""
        overlapping = set(texts).intersection(self._dict)
        if overlapping:
            raise ValueError(f"Tried to add ids that already exist: {overlapping}")
        self._dict = dict(self._dict, **texts)

    def search(self, search: str) -> Union[str, Document]:
        """Search via direct lookup."""
        if search not in self._dict:
            return f"ID {search} not found."
        else:
            return self._dict[search]