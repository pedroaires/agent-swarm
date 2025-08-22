from __future__ import annotations

import logging
from typing import List, Optional

from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)


class VectorRetriever:
    """
    Conects to a already persisted Chroma:
      - as_retriever(): LangChain's BaseRetriever
      - retrieve(query, k): Documents list
    """

    def __init__(
        self,
        *,
        persist_directory: str = "./app/data/chroma_db",
        embeddings: Optional[OpenAIEmbeddings] = None,
    ) -> None:
        self.persist_directory = persist_directory
        self._embeddings = embeddings or OpenAIEmbeddings()
        self._vs: Optional[Chroma] = None

    def load(self) -> bool:
        try:
            self._vs = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self._embeddings,
            )
            logger.info("Vector store loadded from %s", self.persist_directory)
            return True
        except Exception as e:
            logger.error("Error when trying to load vector store: %s", e)
            self._vs = None
            return False

    def as_retriever(self):
        if not self._vs:
            raise RuntimeError("Vector store not loaded. Call load().")
        return self._vs.as_retriever()

    def retrieve(self, query: str, k: int = 8) -> List[Document]:
        if not self._vs:
            raise RuntimeError("Vector store not loaded. Call load().")
        return self._vs.similarity_search(query, k=k)

    @staticmethod
    def format_docs(docs: List[Document]) -> str:
        return "\n\n".join(d.page_content for d in docs)
