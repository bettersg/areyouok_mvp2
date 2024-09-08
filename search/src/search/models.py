import uuid
from datetime import UTC
from datetime import datetime
from typing import Self

from pydantic import BaseModel
from pydantic import model_validator


class Document(BaseModel):
    title: str
    content: str
    metadata: dict = {}
    embedding: list[float] = []
    doc_id: str = None
    timestamp: datetime = datetime.now(UTC)

    @model_validator(mode="after")
    def validate_doc_id(self) -> Self:
        if self.doc_id is None:
            self.doc_id = str(uuid.uuid4())
        return self


class DocumentResponse(BaseModel):
    document_id: str
    timestamp: datetime
