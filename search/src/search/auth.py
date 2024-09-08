import os
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


async def authenticate_user(username: str, password: str):
    if username != os.getenv("POSTGRES_USER"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if password != os.getenv("POSTGRES_PASSWORD"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


async def authenticate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise cred_exception
        exp_time = payload.get("exp")
        if exp_time and datetime.fromtimestamp(exp_time, UTC) < datetime.now(UTC):
            raise cred_exception
    except jwt.InvalidTokenError as e:
        raise cred_exception from e

    if username != os.getenv("POSTGRES_USER"):
        raise cred_exception

    return username


def create_access_token(username: str):
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt
