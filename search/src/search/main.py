import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from psycopg_pool import AsyncConnectionPool
from search.auth import Token
from search.auth import authenticate_token
from search.auth import authenticate_user
from search.auth import create_access_token
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

POSTGRES_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(lifespan=lifespan)


@app.post("/token", response_model=Token, tags=["auth"])
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    await authenticate_user(data.username, data.password)

    access_token = create_access_token(data.username)
    return Token(access_token=access_token, token_type="bearer")


app.include_router(documents_router, dependencies=[Depends(authenticate_token)])
