import certifi # <-- Ensures this library is available
import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from .routers import chat
import motor.motor_asyncio
from dotenv import load_dotenv
from .rag_service import RAGService

from pathlib import Path
# ... other imports
from dotenv import load_dotenv

# This creates a path that points directly to your .env file
env_path = Path('.') / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(
    title="FinEase Bilingual Web-RAG Backend",
    version="4.0.0",
)

# vvvvvv REPLACE your old code with this block vvvvvv

origins = [
    "https://fin-ease.vercel.app",  # Your main Production URL
    "https://fin-ease-qf8iccyk1-nandini-ns-projects.vercel.app", # Your LATEST Preview URL
    "http://localhost:3000",          # For local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ^^^^^^ END of block to replace ^^^^^^

# --- Global Services ---
client = None
database = None
rag_service = RAGService()
SESSIONS = {}

# --- Pydantic Models ---
class ProcessUrlsRequest(BaseModel):
    urls: List[str]

class ChatRequest(BaseModel):
    session_id: str
    question: str
    language: str # 'en' or 'kn'

# --- Database Connection ---
@app.on_event("startup")
async def startup_db_client():
    global client, database
    mongo_url = os.getenv("MONGO_URL")
    if not mongo_url:
        raise ValueError("MONGO_URL environment variable is required.")

    # --- THIS IS THE CRITICAL FIX ---
    # We add the tlsCAFile argument to tell the client where to find trusted certificates.
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url, tlsCAFile=certifi.where())
    # --- END OF FIX ---
    

    database = client["chatbotdb"] # Use your database name, e.g., "FinEaseDB"
    
    # This ping command will now use the secure connection to verify
    try:
        await database.command('ping')
        print("INFO: Successfully connected to MongoDB for FAQ Chatbot!")
    except Exception as e:
        print(f"ERROR: Could not connect to MongoDB. Please check your connection string and firewall settings. Error: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()

# --- API Routers and Endpoints (Your code is unchanged below this line) ---
app.include_router(chat.router, prefix="/api")

@app.post("/api/process-urls")
async def process_urls_for_rag(request: ProcessUrlsRequest):
    if len(request.urls) != 2:
        raise HTTPException(status_code=400, detail="Please provide exactly two URLs.")
    session_id = str(uuid.uuid4())
    vector_stores = [rag_service.create_vector_store_from_url(url) for url in request.urls]
    if any(vs is None for vs in vector_stores):
        raise HTTPException(status_code=500, detail="Failed to process one or more URLs.")
    
    SESSIONS[session_id] = {
        "rag_chain_doc1": rag_service.create_rag_chain(vector_stores[0]),
        "rag_chain_doc2": rag_service.create_rag_chain(vector_stores[1]),
    }
    return {"session_id": session_id}

@app.post("/api/document-chat")
async def chat_with_rag_documents(request: ChatRequest):
    if request.session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Invalid session ID.")
    
    session_data = SESSIONS[request.session_id]
    
    chain_input = {"question": request.question, "language": request.language}
    
    try:
        answer_doc1 = session_data["rag_chain_doc1"].invoke(chain_input)
        answer_doc2 = session_data["rag_chain_doc2"].invoke(chain_input)
        
        final_prompt_template = """
        You are a financial analyst. You have analyzed two financial products from two different websites.
        Based ONLY on the information provided below, provide a clear, final answer.
        First, summarize the findings for the user's question from both websites.
        Then, provide a concluding comparison or recommendation.
        **IMPORTANT**: Your entire final response MUST be in the following language: {language}

        USER'S QUESTION: "{question}"
        INFORMATION FROM WEBSITE A: "{answer1}"
        INFORMATION FROM WEBSITE B: "{answer2}"

        FINAL ANALYSIS (in {language}):
        """
        final_prompt = final_prompt_template.format(
            language=request.language,
            question=request.question,
            answer1=answer_doc1,
            answer2=answer_doc2
        )
        
        final_answer = rag_service.llm.invoke(final_prompt).content
        return {"answer": final_answer}
    except Exception as e:
        print(f"Error during RAG chain invocation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "FinEase Web-RAG Backend is running!"}