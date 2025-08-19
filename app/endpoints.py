from typing import Dict
from fastapi import APIRouter
from app.dtos import ProcessMessageResponseDTO

router = APIRouter()

@router.get("/health", summary="Healthcheck")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@router.get("/process_message", response_model=ProcessMessageResponseDTO, summary="Uses agents to respond to a user request message")
def process_message() -> ProcessMessageResponseDTO:
    return ProcessMessageResponseDTO(response="Agent Message", source_agent_response="Source Agent Response", agent_workflow="Agent Workflow")
