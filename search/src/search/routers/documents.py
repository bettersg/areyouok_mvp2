from fastapi import APIRouter
from fastapi import Request
from search.crud import documents
from search.models import Document
from search.models import DocumentResponse

router = APIRouter(tags=["documents"], prefix="/documents")


@router.get(
    "/{doc_id}",
    response_model=Document | None,
    summary="Gets a document by ID.",
)
async def get_doc_by_id(request: Request, doc_id: str):
    doc = await documents.get(request.app.state.database, doc_id)
    return doc


@router.post(
    "/add",
    response_model=DocumentResponse,
    summary="Adds a document to the database.",
)
async def add_document(request: Request, document: Document):
    await documents.add(request.app.state.database, document)

    resp = DocumentResponse(
        document_id=document.doc_id,
        timestamp=document.timestamp,
    )
    return resp
