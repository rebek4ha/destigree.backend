from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
import json

# Load API key from environment variable
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass  # dotenv is optional

# Initialize FastAPI app
app = FastAPI(title="Destigree API")

# Configure CORS to allow Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#Initialize GROQ client
api_key=os.getenv("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ API KEY not found in the environment variables!")
client = Groq(api_key=api_key)

@app.post("/api/generate")
async def generate_response(request: dict):
    # Get the user's prompt
    user_prompt = request.get("prompt", "")
    
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Please provide a 'prompt' in your request")

