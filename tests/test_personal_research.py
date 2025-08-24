import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

def test_personal_research_ask():
    payload = {
        "query": "What are the latest benchmarks for LLM-based scientific agents?",
        "max_web_results": 2,
        "use_rag": False
    }
    with client.stream("POST", "/api/personal_research/ask", json=payload) as resp:
        assert resp.status_code == 200
        lines = []
        for i, line in enumerate(resp.iter_lines()):
            if line:
                lines.append(line)
            if i > 5:  # Only read a few lines to avoid infinite loop
                break
        assert any(b'"type": "token"' in l for l in lines)
        assert any(b'"type": "sources"' in l for l in lines)
