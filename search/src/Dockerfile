FROM python:3.12.4

COPY --from=ghcr.io/astral-sh/uv:0.3.0 /uv /bin/uv

WORKDIR /api

COPY ./requirements.txt .
RUN uv pip install --system "psycopg[binary]" \
    && uv pip install --system -r requirements.txt

COPY ./src/search /api/search

EXPOSE 8100

CMD ["uvicorn", "search.main:app", \
    "--reload", \
    "--host", "0.0.0.0", \
    "--port", "8100"]