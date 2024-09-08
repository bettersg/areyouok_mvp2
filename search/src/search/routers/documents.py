from fastapi import APIRouter
from fastapi import HTTPException
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


@router.put(
    "/{doc_id}/delete",
    summary="Deletes a document by ID.",
)
async def delete_doc_by_id(request: Request, doc_id: str):
    find_doc = await get_doc_by_id(request, doc_id)
    if not find_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    await documents.delete(request.app.state.database, doc_id)
    return DocumentResponse(
        document_id=doc_id,
        timestamp=find_doc.timestamp,
        status="deleted",
    )


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
        status="added",
    )
    return resp
