from pydantic import BaseModel
from typing import Optional

class ProcessMessageResponseDTO(BaseModel):
    response: str
    source_agent_response: str
    agent_workflow: str

class ProcessMessageRequestDTO(BaseModel):
    message: str
    user_id: str

class IngestRequestDTO(BaseModel):
    urls: Optional[list[str]] | None = None