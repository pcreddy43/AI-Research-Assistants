import os
from typing import Dict, Any, List
from typing import Tuple
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableMap, RunnableLambda
from langchain.schema import Document

from common.langchain_stack import (
    get_search_tool, retrieve, normalize_sources, StackConfig
)

# Choose an LLM — OpenAI by default (swap if needed)
from langchain_openai import ChatOpenAI  # pip install openai langchain-openai

SYSTEM = """You are a precise research assistant. 
- Read the provided web results and retrieved context only.
- Synthesize a concise answer (<= 180 words).
- Add a short bulleted list (3–6 bullets) of key points.
- Cite with [n] bracket indices mapping to the 'sources' array provided (1-based).
- If uncertain, say so and point to sources.
"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("human", """Query: {query}

== Context ==
{context}

== Sources ==
{sources_indexed}

Write the answer and bullets. Use [1], [2], ... to cite sources inline.
""")
])

class ChainRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    max_web_results: int = 5
    use_rag: bool = True
    collection: str = "personal_research_default"
    model: str = "gpt-4o-mini"
    temperature: float = 0.2

def _format_context(docs: List[Document]) -> str:
    lines = []
    for d in docs[:8]:
        meta = d.metadata or {}
        tag = f"{meta.get('source') or meta.get('url') or meta.get('file_path') or ''}"
        snippet = (d.page_content or "").replace("\n", " ")
        lines.append(f"- {snippet[:350]}  (src: {tag})")
    return "\n".join(lines) if lines else "No RAG context."

def _index_sources(web: List[dict], rag_docs: List[Document]) -> Tuple[str, List[dict]]:
    # Build combined sources for indices [1..N]
    sources = []
    for w in web:
        if isinstance(w, dict):
            sources.append({
                "title": w.get("title") or "Untitled",
                "url": w.get("url") or "",
                "snippet": w.get("content", "")[:280]
            })
        elif isinstance(w, str):
            sources.append({
                "title": w[:60] + ("..." if len(w) > 60 else ""),
                "url": "",
                "snippet": w[:280]
            })
        else:
            sources.append({
                "title": "Untitled",
                "url": "",
                "snippet": str(w)[:280]
            })
    # Add RAG doc pseudo-URLs for transparency
    for d in rag_docs[:5]:
        meta = d.metadata or {}
        title = meta.get("title") or meta.get("source") or meta.get("file_path") or "Local document"
        url = meta.get("url") or (meta.get("source") if isinstance(meta.get("source"), str) else "")
        sources.append({"title": title, "url": url, "snippet": d.page_content[:280]})
    # Turn into a numbered list string for the prompt
    lines = [f"[{i+1}] {s['title']} — {s['url']}" for i, s in enumerate(sources)]
    return "\n".join(lines) if lines else "No sources.", sources

def build_chain(req: ChainRequest):
    cfg = StackConfig()
    llm = ChatOpenAI(model=req.model, temperature=req.temperature)

    def run_search(inputs: Dict[str, Any]) -> Dict[str, Any]:
        tool = get_search_tool(k=inputs.get("max_web_results", 5))
        raw = tool.invoke({"query": inputs["query"]})  # returns list[dict]
        return {"web_results": raw}

    def run_rag(inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not inputs.get("use_rag", True):
            return {"rag_docs": []}
        docs = retrieve(inputs["query"], collection=inputs.get("collection", "personal_research_default"), k=6)
        return {"rag_docs": docs}

    gather = RunnableParallel(
        web_results=RunnableLambda(run_search),
        rag=RunnableLambda(run_rag),
    )

    def pack_prompt(inputs: Dict[str, Any]) -> Dict[str, Any]:
        web_items_dict = inputs["web_results"]["web_results"]
        # Extract rag_docs from inputs (fixes scoping error)
        rag_docs = inputs.get('rag', {}).get('rag_docs', [])
        print(f"[pack_prompt] input keys: {list(inputs.keys())}")
        if isinstance(web_items_dict, dict) and "results" in web_items_dict:
            web_items = web_items_dict["results"]
        else:
            web_items = []
        print("DEBUG web_items:", web_items, type(web_items))
        if isinstance(web_items, list) and web_items and isinstance(web_items[0], str):
            web_items = [{"title": w, "url": "", "content": ""} for w in web_items]
        elif not isinstance(web_items, list):
            web_items = []
        sources_indexed, combined_sources = _index_sources(web_items, rag_docs)
        context = _format_context(rag_docs)
        return {
            "query": inputs.get("query", ""),
            "context": context,
            "sources_indexed": sources_indexed,
            "__sources": combined_sources,
        }

    chain = (
        RunnableMap({"query": lambda x: x["query"], "max_web_results": lambda x: x["max_web_results"], "use_rag": lambda x: x["use_rag"], "collection": lambda x: x["collection"]})
        | gather
        | RunnableLambda(pack_prompt)
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain
