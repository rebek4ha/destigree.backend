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