from __future__ import annotations

import logging
from typing import Iterable, List, Optional

from app.core.config import get_config
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)

DEFAULT_URLS: List[str] = [
    "https://www.infinitepay.io",
    "https://www.infinitepay.io/maquininha",
    "https://www.infinitepay.io/maquininha-celular",
    "https://www.infinitepay.io/tap-to-pay",
    "https://www.infinitepay.io/pdv",
    "https://www.infinitepay.io/receba-na-hora",
    "https://www.infinitepay.io/gestao-de-cobranca-2",
    "https://www.infinitepay.io/gestao-de-cobranca",
    "https://www.infinitepay.io/link-de-pagamento",
    "https://www.infinitepay.io/loja-online",
    "https://www.infinitepay.io/boleto",
    "https://www.infinitepay.io/conta-digital",
    "https://www.infinitepay.io/conta-pj",
    "https://www.infinitepay.io/pix",
    "https://www.infinitepay.io/pix-parcelado",
    "https://www.infinitepay.io/emprestimo",
    "https://www.infinitepay.io/cartao",
    "https://www.infinitepay.io/rendimento",
]


def build_index(
    urls: Optional[Iterable[str]] = None,
    *,
    persist_directory: str = "./app/data/chroma_db",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    embeddings: Optional[OpenAIEmbeddings] = None,
) -> None:
    """
    Executes ingestion and create/update the index persisted in Chroma.
    """
    cfg = get_config()
    if not cfg.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set up.")

    use_urls = list(urls) if urls else list(DEFAULT_URLS)
    logger.info("Insgestion: loading %d URLs", len(use_urls))

    docs = WebBaseLoader(use_urls).load()
    logger.info("Ingestion: %d documents loaded", len(docs))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    logger.info("Ingestion: %d chunks", len(chunks))

    embs = embeddings or OpenAIEmbeddings()
    
    Chroma.from_documents(
        documents=chunks,
        embedding=embs,
        persist_directory=persist_directory,
    )
    logger.info("Igestion ended. Index persisted in %s", persist_directory)
