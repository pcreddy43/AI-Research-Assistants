import json
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agents.personal_research.chain import build_chain, ChainRequest
from common.langchain_stack import normalize_sources

router = APIRouter(tags=["personal_research"])

class AskRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    max_web_results: int = 5
    use_rag: bool = True
    collection: str = "personal_research_default"
    model: str = "gpt-4o-mini"
    temperature: float = 0.2

def _ndjson(obj: Dict[str, Any]) -> bytes:
    return (json.dumps(obj) + "\n").encode("utf-8")

@router.post("/personal_research/ask")
def ask(req: AskRequest):
    chain = build_chain(ChainRequest(**req.dict()))
    try:
        output_text = chain.invoke(req.dict())
    except Exception as e:
        import traceback
        print("ERROR in chain.invoke:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    from agents.personal_research.chain import _index_sources as _idx, _format_context as _fmt
    from common.langchain_stack import get_search_tool, retrieve

    try:
        web = get_search_tool(k=req.max_web_results).invoke({"query": req.query})
        print("Web search results:", web)
        rag_docs = retrieve(req.query, collection=req.collection, k=6) if req.use_rag else []
        print("RAG docs:", rag_docs)
        _, combined_sources = _idx(web.get("results", []), rag_docs)
        print("Combined sources:", combined_sources)
    except Exception as e:
        import traceback
        print("ERROR in source retrieval:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    async def gen():
        chunk = 800
        text = output_text if output_text is not None else ""
        if not isinstance(text, str):
            text = str(text)
        for i in range(0, len(text), chunk):
            yield _ndjson({"type": "token", "text": text[i:i+chunk]})
        print("Yielding sources:", combined_sources)
        yield _ndjson({"type": "sources", "items": combined_sources})
        yield _ndjson({"type": "done"})

    return StreamingResponse(gen(), media_type="application/x-ndjson")
