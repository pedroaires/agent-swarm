from pydantic import BaseModel

class ProcessMessageResponseDTO(BaseModel):
    response: str
    source_agent_response: str
    agent_workflow: str

class ProcessMessageRequestDTO(BaseModel):
    message: str
    user_id: str