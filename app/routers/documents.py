from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas import (
    DocumentCreate,
    DocumentResponse,
)

from app.services.document_service import (
    add_document,
    get_documents,
    delete_document,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are allowed."
        )

    try:
        content = await file.read()

        content = content.decode("utf-8")

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="The TXT file must use UTF-8 encoding."
        )

    if not content.strip():
        raise HTTPException(
            status_code=400,
            detail="The TXT file is empty."
        )

    document = DocumentCreate(
        filename=file.filename,
        content=content
    )

    return add_document(document)


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents():

    try:

        return get_documents()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.delete(
    "/{document_id}",
    response_model=DocumentResponse,
)
def remove_document(
    document_id: str,
):

    try:

        document = delete_document(
            document_id
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        return document

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )