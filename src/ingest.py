import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from database import add_documents

load_dotenv()

PDF_PATH = os.getenv('PDF_PATH', Path(__file__).resolve().parents[1] / 'document.pdf')

def _ingest_pdf():
    if not os.path.isfile(PDF_PATH):
        raise FileNotFoundError(f'Specified PDF file not found in: {PDF_PATH}')

    print(f'Ingesting PDF file from: {PDF_PATH}')

    document = PyPDFLoader(PDF_PATH).load()

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    ).split_documents(document)

    print('Converting chunks into documents')

    documents = [
        Document(
            page_content=chunk.page_content,
            metadata={k: v for k, v in chunk.metadata.items() if v not in ('', None)}
        ) for chunk in chunks
    ]

    print(f'Adding {len(documents)} documents to the database')

    add_documents(documents)

    print('Ingestion completed successfully')

if __name__ == '__main__':
    _ingest_pdf()
