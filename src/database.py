import os
from dotenv import load_dotenv
from models import get_embedding_model
from langchain_postgres import PGVector
from uuid import uuid4

load_dotenv()

def _build_store():
    embeddings = get_embedding_model()

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv('PG_VECTOR_COLLECTION_NAME', 'documents'),
        connection=os.getenv('PG_VECTOR_DATABASE_URL', 'postgresql+psycopg://postgres:postgres@localhost:5432/rag'),
        use_jsonb=True,
    )

    return store

def add_documents(documents):
    store = _build_store()

    store.add_documents(
        documents=documents,
        ids=[str(uuid4()) for _ in range(len(documents))]
    )

def similarity_search(question, k=10):
    store = _build_store()

    documents = store.similarity_search(question , k=k)

    return [document.page_content.strip() + '\n' for document in documents]
