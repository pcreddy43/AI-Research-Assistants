from app.metrics.metrics import LLM_TIME, RAG_TIME, WEB_SEARCH_TIME, AGENT_REQUESTS
from app.app_utils.retry import retry
import concurrent.futures
from typing import Dict, Any

def research_agent_parallel(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("question", "")
    results = []
    AGENT_REQUESTS.inc()

    @retry(max_attempts=3, backoff=1.0)
    @WEB_SEARCH_TIME.time()
    def web_search(q):
        # Simulate possible flaky network call
        return f"Web result for: {q}"

    @RAG_TIME.time()
    def rag_search(q):
        return f"RAG result for: {q}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_web = executor.submit(web_search, query)
        future_rag = executor.submit(rag_search, query)
        results.append(future_web.result())
        results.append(future_rag.result())

    return {"research_results": results}
