from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.personal_research import router as research_router
from api.upload import router as upload_router


app = FastAPI(title="AgenticAI API")

app.include_router(upload_router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_router, prefix="/api")

@app.get("/health")
def health():
    return {"ok": True}
