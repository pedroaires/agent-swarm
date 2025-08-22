from typing import Dict
from fastapi import APIRouter
from app.api.dtos import ProcessMessageResponseDTO, ProcessMessageRequestDTO, IngestRequestDTO
from app.rag.ingestion import build_index

router = APIRouter()


@router.get("/health", summary="Healthcheck")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@router.get("/process_message", response_model=ProcessMessageResponseDTO, summary="Uses agents to respond to a user request message")
def process_message() -> ProcessMessageResponseDTO:
    return ProcessMessageResponseDTO(response="Agent Message", source_agent_response="Source Agent Response", agent_workflow="Agent Workflow")

@router.post("/ingest", summary="Endpoint to execute RAG ingestion phase.")
def ingest(req: IngestRequestDTO) -> Dict[str, str]:
    build_index(req.urls)
    return {"status": "ok"}

# @router.post("/rag", summary="Endpoint to execute RAG QA to test RAG.")
# def rag(req: ProcessMessageRequestDTO) -> Dict[str, str]:
#     answer = rag_service.ask(req.message)
#     return {"status": "ok", "answer": answer}