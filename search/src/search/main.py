import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from psycopg_pool import AsyncConnectionPool

from search.routers import documents_router

EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536,
    api_key=os.getenv("OPENAI_API_KEY"),
)

CHUNKER = SemanticChunker(
    embeddings=EMBEDDINGS,
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=0.5,
)

POSTGRES_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/terra"
POSTGRES = AsyncConnectionPool(POSTGRES_URL, open=False)

LOGGER = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = LOGGER
    app.state.text_splitter = CHUNKER
    app.state.text_embedder = EMBEDDINGS

    app.state.database = POSTGRES

    await app.state.database.open()
    app.state.logger.info("Database and cache connections established.")

    yield

    await app.state.database.close()


app = FastAPI(lifespan=lifespan)

app.include_router(documents_router)
