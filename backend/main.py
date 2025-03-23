import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables with better error handling
# In Cloud Run, we'll use environment variables directly rather than .env files
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    # Try to find .env in parent directory if in backend subdirectory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    potential_dotenv = os.path.join(parent_dir, '.env')
    if os.path.exists(potential_dotenv):
        load_dotenv(potential_dotenv)

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # In production environment, we'll print a warning instead of exiting
    # This allows the container to start even if API key is provided at runtime
    print("WARNING: OpenAI API key not found!")
    print("Please provide the OPENAI_API_KEY environment variable.")
    if not os.getenv("PRODUCTION", False):
        sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Wizard Trainer API",
    description="API for training wizardly speaking patterns",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware with Cloud Run support
app.add_middleware(
    CORSMiddleware,
    # Allow local development and Cloud Run URLs
    allow_origins=["http://localhost:5173", "http://localhost:4173", "http://localhost:3000", 
                   "http://localhost:8000", "http://localhost:8080", "https://*.run.app"],
    allow_origin_regex=r"https://.*-[a-z0-9]+\.run\.app",  # Allow all Cloud Run domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Models
class TextRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    original_text: str
    wizard_texts: List[str]  # Changed from wizard_text to wizard_texts (plural)

class JudgementResponse(BaseModel):
    text: str
    score: int
    feedback: str
    suggestions: List[str]

# Helper functions
async def generate_wizard_text(text: str) -> List[str]:
    """Use OpenAI to translate text into multiple wizard speech options"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                        "You are a translator that converts ordinary text into the speech of a wise, mystical wizard from fantasy literature. "
                        "Use archaic terms, magical references, and a grandiose style. "
                        "Replace modern terms with magical equivalents when possible."
                    )
                },
                {"role": "user", "content": (
                        "Translate this text into wizard speech. "
                        "Make sure to persevere the original meaning. "
                        "Provide THREE distinct variations with different styles. "
                        "Return your response as a JSON object with the format: {{\"translations\": [\"variation1\", \"variation2\", \"variation3\"]}}. "
                        "Make each one unique in tone and vocabulary: {text}"
                    )
                }
            ],
            max_tokens=800,
            temperature=0.7,  # Adjusted for more creative output
            response_format={"type": "json_object"}  # Explicitly request JSON response
        )
        result = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        import json
        try:
            json_response = json.loads(result)
            translations = json_response.get("translations", [])
            
            # Ensure we have exactly 3 translations
            if len(translations) < 3:
                # If we got fewer than 3, duplicate the last one to fill
                while len(translations) < 3:
                    translations.append(translations[-1] if translations else "By the ancient scrolls, the message remains unclear.")
            elif len(translations) > 3:
                # If we got more than 3, keep only the first 3
                translations = translations[:3]
                
            return translations
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            print(f"Failed to parse JSON response: {result}")
            return [
                "By the ancient scrolls, I sense a disturbance in the magical flow.",
                "Hark! The ethereal translation incantation seems to have faltered.",
                "As the stars foretold, our mystical communication has encountered a barrier."
            ]
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

async def judge_wizard_speech(text: str) -> dict:
    """Use OpenAI to judge how wizard-like the text sounds"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "You are a judge evaluating how well someone speaks like a fantasy wizard. "
                    "You will rate the text on a scale of 1-10, provide feedback, and offer specific suggestions for improvement. "
                    "Value creativity, use of archaic language, and overall wizardly flair."
                    "Bonus points for humor, whimsy, and the use of mysterious aphorisms or wisened statments."
                    "If the text is a low score (<= 3), feel free to lightly mock it as a wizard would."
                    "Respond with a JSON object with fields 'score' (integer 1-10), 'feedback' (string), and 'suggestions' (array of strings).")},
                {"role": "user", "content": f"Evaluate this text for wizard-like qualities: {text}"}
            ],
            max_tokens=500,
            temperature=0.25  # Lower temperature for more consistent results
        )
        result_text = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        import json
        try:
            result = json.loads(result_text)
            return {
                "score": int(result.get("score", 5)),
                "feedback": result.get("feedback", ""),
                "suggestions": result.get("suggestions", [])
            }
        except json.JSONDecodeError:
            # Fallback if response isn't valid JSON
            return {
                "score": 5,
                "feedback": "Your speech has some wizardly qualities, but the ancient magic prevents a full assessment.",
                "suggestions": ["Add more arcane references", "Use more antiquated language"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

# Routes
@app.post("/api/translate", response_model=TranslationResponse)
async def translate_text(request: TextRequest):
    """Translate normal text to wizard speech with three options."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    wizard_texts = await generate_wizard_text(request.text)
    
    return TranslationResponse(
        original_text=request.text,
        wizard_texts=wizard_texts
    )

@app.post("/api/judge", response_model=JudgementResponse)
async def judge_text(request: TextRequest):
    """Judge how wizard-like the text sounds."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = await judge_wizard_speech(request.text)
    
    return JudgementResponse(
        text=request.text,
        score=result["score"],
        feedback=result["feedback"],
        suggestions=result["suggestions"]
    )

# Update the root route to include deployment information
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Wizard Trainer API",
        "environment": "Production" if os.getenv("PRODUCTION", False) else "Development",
        "documentation": "/docs"
    }

# For Google Cloud Run, which uses PORT environment variable
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

