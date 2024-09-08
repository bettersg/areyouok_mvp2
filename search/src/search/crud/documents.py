import json

from psycopg_pool import AsyncConnectionPool
from search.models import Document

from . import sql


async def get(database: AsyncConnectionPool, doc_id: str) -> Document | None:
    async with database.connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql.FETCH_DOCUMENT, (doc_id,))
            raw_data = await cursor.fetchone()
            if raw_data is None:
                return None

            return Document(
                doc_id=raw_data[0],
                timestamp=raw_data[1],
                last_updated=raw_data[2],
                title=raw_data[3],
                content=raw_data[4],
                metadata=json.loads(raw_data[5]),
                embedding=json.loads(raw_data[6]),
            )


async def add(database: AsyncConnectionPool, document: Document):
    async with database.connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                sql.INSERT_DOCUMENT,
                (
                    document.doc_id,
                    document.timestamp,
                    document.timestamp,  # last_updated
                    document.title,
                    document.content,
                    json.dumps(document.metadata),
                    json.dumps(document.embedding),
                ),
            )
