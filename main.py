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