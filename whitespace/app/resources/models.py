from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str
    model: Optional[str] = None

    def to_openai_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }


class ChatParameters(BaseModel):
    model: str
    temperature: float
    sys_prompt: str
    id: str = str(uuid4())
    messages: list[ChatMessage] = []
