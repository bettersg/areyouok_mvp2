INSERT_DOCUMENT = """
    INSERT INTO raw.documents (
        doc_id,
        timestamp,
        last_updated,
        title,
        content,
        metadata,
        embedding
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (doc_id) DO UPDATE
    SET last_updated = EXCLUDED.last_updated,
        title = EXCLUDED.title,
        content = EXCLUDED.content,
        metadata = EXCLUDED.metadata,
        embedding = EXCLUDED.embedding;
    """

FETCH_DOCUMENT = """
    SELECT
        doc.doc_id,
        doc.timestamp,
        doc.last_updated,
        doc.title,
        doc.content,
        doc.metadata,
        doc.embedding
    FROM
        raw.documents as doc
    WHERE
        doc.doc_id = %s;
    """
