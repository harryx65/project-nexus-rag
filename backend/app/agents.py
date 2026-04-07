from dataclasses import dataclass, field
from typing import Any, Dict, List

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os

from app.config import DEFAULT_LLM_REPO


@dataclass
class AgentEvent:
    name: str
    payload: Dict[str, Any] = field(default_factory=dict)


# Load model once

def get_llm():
    llm_raw = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-120b",
        task="text-generation",
        max_new_tokens=500,
        temperature=0.2,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
    )

    return ChatHuggingFace(llm=llm_raw)


class ResearcherAgent:
    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, question: str) -> AgentEvent:
        docs = self.retriever.invoke(question)

        context_parts = []
        citations = []

        for index, doc in enumerate(docs, start=1):
            file_name = doc.metadata.get("file_name", "Unknown file")
            page = doc.metadata.get("page", 0)
            context_parts.append(doc.page_content)
            citations.append(
                {
                    "id": index,
                    "file_name": file_name,
                    "page": page + 1,
                    "snippet": doc.page_content[:220].strip()
                }
            )

        return AgentEvent(
            name="research.completed",
            payload={
                "question": question,
                "context": "\n\n".join(context_parts),
                "citations": citations,
                "documents": docs,
            }
        )


class CriticAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, research_event: AgentEvent) -> AgentEvent:
        question = research_event.payload["question"]
        context = research_event.payload["context"]
        citations = research_event.payload["citations"]

        prompt = f"""
You are the critic agent inside a RAG system.
Your job is to answer only from the provided context.
If the context is weak or incomplete, say that clearly.
Do not make up facts.
Give a direct answer first, then a short verification note.

Question:
{question}

Context:
{context}
"""

        response = self.llm.invoke(prompt)
        answer = response.content.strip()

        if not citations:
            answer = "I could not find enough information in the uploaded documents."

        return AgentEvent(
            name="critic.completed",
            payload={
                "answer": answer,
                "citations": citations,
            }
        )


class RAGWorkflow:
    def __init__(self, retriever):
        self.llm = get_llm()
        self.researcher = ResearcherAgent(retriever)
        self.critic = CriticAgent(self.llm)

    def run(self, question: str) -> List[AgentEvent]:
        events = []

        start_event = AgentEvent(name="question.received", payload={
                                 "question": question})
        events.append(start_event)

        research_event = self.researcher.run(question)
        events.append(research_event)

        critic_event = self.critic.run(research_event)
        events.append(critic_event)

        return events
