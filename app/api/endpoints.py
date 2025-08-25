from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.api.dtos import ProcessMessageResponseDTO, ProcessMessageRequestDTO, IngestRequestDTO
from app.rag.ingestion import build_index
from app.agents.workflow import build_graph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document

router = APIRouter()
_GRAPH = build_graph()

@router.get("/health", summary="Healthcheck")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@router.post("/process_message", response_model=ProcessMessageResponseDTO, summary="Uses agents to respond to a user request message")
def process_message(req: ProcessMessageRequestDTO) -> Dict[str, str]:
    if not req.message:
        raise HTTPException(status_code=400, detail="User message is required")
    if not req.user_id:
        raise HTTPException(status_code=400, detail="User Id is required")

    init = {"messages": [HumanMessage(content=req.message)]}
    config = {"configurable": {
        "thread_id": req.user_id ,
        "user_id": req.user_id
        }}

    state = _GRAPH.invoke(init, config=config)
    msgs = state.get("messages", [])
    if not msgs:
        raise HTTPException(status_code=500, detail="Empty response from agent swarm")

    final_answer = msgs[-1].content
    return {"response": final_answer}

@router.post("/ingest", summary="Endpoint to execute RAG ingestion phase.")
def ingest(req: IngestRequestDTO) -> Dict[str, str]:
    build_index(req.urls)
    return {"status": "ok"}

