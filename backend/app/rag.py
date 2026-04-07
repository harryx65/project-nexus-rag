from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHROMA_FOLDER, DEFAULT_EMBEDDING_MODEL


# Load PDF files

def load_pdf_files(data_folder: Path) -> List[Document]:
    documents = []

    for file_path in data_folder.rglob("*.pdf"):
        loader = PyPDFLoader(str(file_path))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = str(file_path)
            doc.metadata["file_name"] = file_path.name

        documents.extend(docs)

    return documents


# Split documents into chunks

def split_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


# Create embeddings

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=DEFAULT_EMBEDDING_MODEL,
    )


# Save to Chroma

def build_vectorstore(data_folder: Path):
    documents = load_pdf_files(data_folder)

    if not documents:
        raise ValueError("No PDF files found in backend/data folder.")

    chunks = split_documents(documents)
    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_FOLDER)
    )

    return vectorstore, len(documents), len(chunks)


# Load existing vectorstore

def load_vectorstore():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=str(CHROMA_FOLDER),
        embedding_function=embeddings
    )
