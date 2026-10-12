from datetime import datetime
from uuid import uuid4
from app.vectorstore.vector_store import VectorStore

from app.database import SessionLocal
from app.models import Document

from app.schemas import (
    DocumentCreate,
    DocumentResponse,
)

from app.utils.text_splitter import (
    clean_text,
    split_text,
)

from app.services.embedding_service import (
    generate_embedding,
)

vector_store = VectorStore()


def add_document(
    document: DocumentCreate,
) -> DocumentResponse:

    db = SessionLocal()

    try:

        document_id = str(uuid4())

        cleaned_content = clean_text(
            document.content
        )

        chunks = split_text(
            cleaned_content
        )

        for chunk_id, chunk in enumerate(chunks):

            vector = generate_embedding(
                chunk
            )

            metadata = {
                "document_id": document_id,
                "document_name": document.filename,
                "chunk_id": chunk_id,
                "text": chunk,
            }

            vector_store.add_vector(
                vector,
                metadata
            )

        created_at = datetime.now()

        db_document = Document(
            id=document_id,
            filename=document.filename,
            content=cleaned_content,
            created_at=created_at,
        )

        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        return DocumentResponse(
            id=db_document.id,
            filename=db_document.filename,
            content=db_document.content,
            created_at=db_document.created_at,
        )

    finally:

        db.close()


def get_documents():

    db = SessionLocal()

    try:

        documents = (
            db.query(Document)
            .all()
        )

        return [
            DocumentResponse(
                id=document.id,
                filename=document.filename,
                content=document.content,
                created_at=document.created_at,
            )
            for document in documents
        ]

    finally:

        db.close()


def delete_document(
    document_id: str,
):

    db = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if document is None:
            return None

        deleted_document = DocumentResponse(
            id=document.id,
            filename=document.filename,
            content=document.content,
            created_at=document.created_at,
        )

        vector_store.delete_document(
            document_id
        )

        db.delete(document)
        db.commit()

        return deleted_document

    finally:

        db.close()