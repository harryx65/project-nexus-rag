from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class UploadResponse(BaseModel):
    message: str
    file_name: str
