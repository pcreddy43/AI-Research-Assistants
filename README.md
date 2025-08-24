# AI-Research-Assistants
The Personal Research Assistant is an AI-powered tool that answers research questions by searching the web and (optionally) your own uploaded documents, then synthesizes a concise, cited answer.

# AgenticAI_VS_Starter_Plus

🚀 A multi-agent AI workspace designed for **research automation, task routing, and workflow orchestration**.  
Built with **FastAPI + LangChain + React**, this project showcases how agentic AI can be applied to real-world problems.

---

## 📌 Features
- **Personal Research Assistant** – RAG-powered, web & scholarly search with citations  
- **Math & Code Solver Agent** – solve equations, algorithms, and coding problems  
- **Chatbot with Memory** – context-aware conversational assistant  
- **Workflow Router Agent** – routes tasks to the right agent  
- **Multi-Model Router Agent** – switch between LLMs dynamically  
- **Debate Agent (Ensemble AI)** – multiple agents argue & refine answers  
- **Web Research Agent** – quick search with summaries  
- **Autonomous Task Planner** – break down goals into subtasks  
- **Customer Support Agent** – domain-specific support  
- **Financial Report Agent** – generate structured financial insights  
- **Enterprise Workflow Agent** – automation for business processes  

---

## 🛠️ Tech Stack
- **Backend**: FastAPI, LangChain, Python  
- **Frontend**: React (Vite + TypeScript, shadcn/ui, TailwindCSS)  
- **RAG**: Chroma (Vector DB), Tavily Search, Arxiv Loader  
- **Agents**: Custom multi-agent orchestration framework  
- **Other Tools**: Docker (optional), PyMuPDF, PDF parsing  

---

## ⚡ Quick Start

### Backend (FastAPI)
```bash
# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn api.main:app --reload --port 8000

## Frontend (React)
cd apps/research-ui
npm install
npm run dev
# Open http://localhost:5173


Project Structure
AgenticAI_VS_Starter_Plus
│── agents/                 # Each agent module
│   ├── personal_research/
│   ├── math_code_solver/
│   ├── ...
│── api/                    # FastAPI endpoints
│── common/                 # Shared utilities
│── apps/research-ui/       # React frontend
│── tests/                  # Unit tests
│── requirements.txt
│── README.md

Ask a research question:

POST /api/personal_research/ask
{
  "query": "Latest progress on diffusion models for robotics?",
  "use_rag": true,
  "max_web_results": 5
}


Response:

🔹 Summarized answer

🔹 Citations with links

🔹 Optional RAG context (PDFs, notes)

🧑‍💻 Author

Pulla C Sekhara Reddy
🎓 AI & Embedded Systems Researcher | Automotive Software | Competitive Programmer

📜 License

This project is licensed under the MIT License
.


---

## 📜 2. LICENSE (MIT License recommended)
```text
MIT License

Copyright (c) 2025 Pulla C Sekhara Reddy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[...standard MIT text continues...]

⚙️ 3. .gitignore (Python + Node/React)
# Python
__pycache__/
*.pyc
.venv/
.env

# Node/React
node_modules/
dist/
.vite/

# Chroma DB
data/chroma/

# OS
.DS_Store
Thumbs.db
