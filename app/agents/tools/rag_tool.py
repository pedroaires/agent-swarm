from langchain.tools import tool
from app.rag.retriever import VectorRetriever

@tool
def rag_tool(query: str) -> str:
    """Use this tool to retrieve information from the internal knowledge base about the company infinite pay. The database is in portuguese, so to enhance the retrieval, you must query in portuguese."""
    retriever = VectorRetriever()
    if not retriever.load():
        return "Error: Could not load vector store for RAG."
    docs = retriever.retrieve(query)
    return VectorRetriever.format_docs(docs)