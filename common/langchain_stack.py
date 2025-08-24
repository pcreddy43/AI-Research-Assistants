import os  # Provides functions for interacting with the operating system
from dataclasses import dataclass  # For creating simple data classes
from typing import List, Dict, Optional, Any  # Type hints for better code clarity and static analysis

from dotenv import load_dotenv  # Loads environment variables from a .env file
load_dotenv()

from langchain_tavily import TavilySearch  # Updated import for Tavily web search
from langchain_community.document_loaders import ArxivLoader  # Loads academic papers from arXiv
from langchain_community.document_loaders import PyPDFLoader  # Loads and parses PDF documents
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Splits text into manageable chunks
from langchain_community.vectorstores import Chroma  # Vector store for efficient similarity search
from langchain_community.embeddings import OpenAIEmbeddings  # Embedding model for text vectorization

from langchain.schema import Document  # Standard document schema for LangChain


def get_search_tool(k: int=5) -> TavilySearch:
    return TavilySearch(max_results=k, include_answer=True, include_raw_content=False, include_images=False)

def load_arxiv(query: str, max_results: int = 5) -> List[Document]:
    loader = ArxivLoader(query=query)
    documents = loader.load()
    return documents[:max_results]

def load_pdf(file_path: str) -> List[Document]:
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()
    return documents

def chunk_docs(docs: List[Document], chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(docs)

def get_embeddings():
    return OpenAIEmbeddings()

DATA_DIR = os.path.join(os.getcwd(), "data")  # Directory to store data files
VECTOR_DIR = os.path.join(DATA_DIR, "Chroma")
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data directory exists
os.makedirs(VECTOR_DIR, exist_ok=True)  # Ensure vector directory exists

def get_vectorstore(collection: str) -> Chroma:
    return Chroma(collection_name=collection, embedding_function=get_embeddings(), persist_directory=VECTOR_DIR)

def index_documents(docs: List[Document], collection: str = "default") -> int:
    if not docs:
        return 0
    vs = get_vectorstore(collection)
    vs.add_documents(docs)
    vs.persist()
    return len(docs)

def normalize_sources(items: list[dict]) -> list[dict]:
    out = []
    for it in items:
        title = it.get("title") or it.get("url") or "Untitled"
        url = it.get("url") or ""
        snippet = it.get("content") or it.get("snippet") or ""
        out.append({"title": title, "url": url, "snippet": snippet[:300]})
    return out

def retrieve(query: str, collection: str = "default", k: int = 6):
    """Retrieve top-k relevant documents from the vectorstore for a given query."""
    # TODO: Implement real retrieval logic using your vectorstore
    # For now, return an empty list or mock documents
    return []

@dataclass
class StackConfig:
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    serpapi_api_key = os.getenv("SERP_API_KEY")
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    # All utility functions are now top-level, so this class is just for config.