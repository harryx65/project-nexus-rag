from dotenv import load_dotenv

from app.config import DATA_FOLDER
from app.rag import build_vectorstore

load_dotenv()


def main():
    print("Loading PDF files...")

    vectorstore, documents_count, chunks_count = build_vectorstore(DATA_FOLDER)

    print(f"Loaded {documents_count} PDF pages/documents.")
    print(f"Created {chunks_count} chunks.")
    print("Ingestion complete!")
    print(f"Vector database ready: {vectorstore._persist_directory}")


if __name__ == "__main__":
    main()
