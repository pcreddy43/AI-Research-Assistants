import os
from fastapi import Header, HTTPException, Depends
from dotenv import load_dotenv

load_dotenv()

API_KEYS = os.environ.get("API_KEYS", "localdev123").split(",")

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key
