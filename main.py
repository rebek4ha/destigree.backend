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
    allow_origins=["http://localhost:4200"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["Content-Type"],  # Allow all headers
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
    
    try:
        # Example major list to show the AI
        major_example = {
            "degree": "Bachelor of Computer Engineering",
            "location": "Canada",
            "reason": "If you are fascinated by how computers and electronics work, enjoy coding, building gadgets, and solving tech challenges, you might be motivated to study computer engineering to create and improve technology.",
            "requirements": "ENG4U/EAE4U, MHF4U, MCV4U, SPH4U & SCH4U",
            "universities": "University of Toronto, University of British Columbia & University of Waterloo",
            "careers": "Software Developer, Hardware Engineer, Cloud Engineer, Data Scientist & Cybersecurity Analyst",
            "salary": "$91,000 - $120,000"
        }   
        #Create the message to send to the API
        message = f"""You are a university major expert.

User wants: {user_prompt}

Respond with exactly 9 university major recommendations in this JSON format:
{{
    "degrees": [
        {json.dumps(major_example, indent=8)},
        ... (9 majors total)
    ]
}}

Rules:
- Exactly 9 university majors
- Accurate degrees, reasons, and requirements
- Brief descriptions (1-2 sentences)
- Top 3 universities that offer those majors based on the location that the user gives
- If location is not put in the prompt, say the location as Canada automatically 
- Return ONLY valid JSON
"""
            # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast and free model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds with valid JSON."},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"},  # Force JSON response
            temperature=0.7
        )
                # Get the AI's response and parse it
        ai_response = response.choices[0].message.content
        result = json.loads(ai_response)
        
        # Return the different uni major recommendations
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "LLM API is running", "status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)