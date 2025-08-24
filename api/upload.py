from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from common.langchain_stack import load_pdf, chunk_docs, index_documents

router = APIRouter(tags=["upload"])

@router.post("/upload")
async def upload(file: UploadFile = File(...), namespace: str = Form("personal_research_default")):
    path = f"data/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    docs = load_pdf(path)
    chunks = chunk_docs(docs)
    n = index_documents(chunks, collection=namespace)
    return JSONResponse({"ok": True, "docId": path, "title": file.filename, "chunks": n})
