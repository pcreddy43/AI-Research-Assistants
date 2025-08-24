from fastapi import FastAPI, Header, HTTPException, UploadFile, File, Request, Depends
from fastapi.responses import StreamingResponse
import asyncio
import json
from typing import Optional
from app.auth import require_api_key
from pydantic import BaseModel
from app.graphs.multi_agent_team import orchestrator, TeamState
from app.graphs.multi_step_flow import controller as multi_step_controller
from app.metrics.metrics import start_metrics_server
from app.nodes.research_agent_parallel import research_agent_parallel

app = FastAPI()

# Streaming endpoint for node events as SSE
from app.graphs.multi_step_flow import streaming_controller

@app.post("/ask_stream")
async def ask_stream(request: Request, x_api_key: Optional[str] = Header(None)):
    if x_api_key != "localdev123":
        raise HTTPException(status_code=401, detail="Invalid API key")
    body = await request.json()
    question = body.get("question")
    session_id = body.get("session_id")

    async def event_generator():
        for event in streaming_controller(question, session_id):
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
from typing import Optional
from pydantic import BaseModel
from app.graphs.multi_agent_team import orchestrator, TeamState
from app.graphs.multi_step_flow import controller as multi_step_controller
from app.metrics.metrics import start_metrics_server

app = FastAPI()

# /upload endpoint for document upload
@app.post("/upload")
async def upload(file: UploadFile = File(...), x_api_key: Optional[str] = Header(None)):
    if x_api_key != "localdev123":
        raise HTTPException(status_code=401, detail="Invalid API key")
    # Save uploaded file to disk (for demonstration)
    file_location = f"uploaded_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    # TODO: Add logic to process and index the document for RAG
    return {"filename": file.filename, "status": "uploaded"}
@app.get("/health")
async def health():
    return {"status": "ok"}

class Query(BaseModel):
    question: str
    session_id: str


@app.post("/team_ask")
async def team_ask(query: Query):
    state = TeamState(question=query.question, session_id=query.session_id)
    result = orchestrator(state)
    return result

# New /ask_multi endpoint with x-api-key header support and multi-step flow
@app.post("/ask_multi")
async def ask_multi(query: Query, api_key: str = Depends(require_api_key)):
    result = multi_step_controller(query.question, query.session_id)
    return result

@app.post("/test_parallel")
async def test_parallel(query: Query, api_key: str = Depends(require_api_key)):
    state = {"question": query.question}
    result = research_agent_parallel(state)
    return result

@app.on_event("startup")
async def startup_event():
    start_metrics_server(8002)
    print("API Started. Visit /docs for Swagger UI.")
