from pathlib import Path
import asyncio
import json
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from app.agents import RAGWorkflow
from app.config import CHROMA_FOLDER, DATA_FOLDER
from app.rag import build_vectorstore, load_vectorstore
from app.schemas import ChatRequest

load_dotenv()

app = FastAPI(title="Project Nexus API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = None


# Load system once

def load_rag_system():
    global workflow

    if not CHROMA_FOLDER.exists():
        raise RuntimeError("Vector database not found. Run ingest.py first.")

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    workflow = RAGWorkflow(retriever)


@app.on_event("startup")
def startup_event():
    try:
        load_rag_system()
    except Exception:
        # app can still start, but chat endpoint will ask to ingest first
        pass


@app.get("/")
def home():
    return {"message": "Project Nexus API is running"}


@app.post("/ingest")
def ingest_documents():
    global workflow

    vectorstore, documents_count, chunks_count = build_vectorstore(DATA_FOLDER)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    workflow = RAGWorkflow(retriever)

    return {
        "message": "Documents ingested successfully",
        "documents": documents_count,
        "chunks": chunks_count,
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    save_path = DATA_FOLDER / file.filename

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "PDF uploaded successfully",
        "file_name": file.filename,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    if workflow is None:
        raise HTTPException(status_code=400, detail="Run /ingest first to prepare the vector database.")

    events = workflow.run(request.question)
    final_payload = events[-1].payload

    return {
        "question": request.question,
        "answer": final_payload["answer"],
        "citations": final_payload["citations"],
        "events": [event.name for event in events],
    }


@app.get("/chat/stream")
async def chat_stream(question: str):
    if workflow is None:
        raise HTTPException(status_code=400, detail="Run /ingest first to prepare the vector database.")

    async def event_generator():
        events = workflow.run(question)
        final_payload = events[-1].payload
        answer = final_payload["answer"]

        for event in events:
            yield {
                "event": "workflow",
                "data": json.dumps({"name": event.name})
            }
            await asyncio.sleep(0.15)

        words = answer.split()
        current_text = []

        for word in words:
            current_text.append(word)
            yield {
                "event": "token",
                "data": json.dumps({"text": " ".join(current_text)})
            }
            await asyncio.sleep(0.03)

        yield {
            "event": "citations",
            "data": json.dumps(final_payload["citations"])
        }

        yield {
            "event": "done",
            "data": json.dumps({"ok": True})
        }

    return EventSourceResponse(event_generator())
