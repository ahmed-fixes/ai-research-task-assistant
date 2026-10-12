from fastapi import FastAPI

from app.routers.agent import router as agent_router
from app.routers.documents import router as documents_router

from app.database import Base, engine


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="AI Research Task Assistant"
)


app.include_router(
    agent_router
)

app.include_router(
    documents_router
)