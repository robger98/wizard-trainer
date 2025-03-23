import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables with better error handling
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
    print("ERROR: OpenAI API key not found!")
    print("Please create a .env file with your OPENAI_API_KEY.")
    print("Example: OPENAI_API_KEY=your_key_here")
    print(f"Place it in: {os.path.dirname(os.path.abspath(__file__))} or {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Wizard Trainer API",
    description="API for training wizardly speaking patterns",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow requests from Svelte frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173", "http://localhost:3000", "http://localhost:8000"],  # Added 8000 for API docs
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a translator that converts ordinary text into the speech of a wise, mystical wizard from fantasy literature. Use archaic terms, magical references, and a grandiose style. Add phrases like 'By the ancient powers', 'As the stars foretold', or 'Hark and listen well'. Replace modern terms with magical equivalents when possible."},
                {"role": "user", "content": f"Translate this text into wizard speech. Provide THREE distinct variations with different styles. Return your response as a JSON object with the format: {{\"translations\": [\"variation1\", \"variation2\", \"variation3\"]}}. Make each one unique in tone and vocabulary: {text}"}
            ],
            max_tokens=800,
            temperature=0.8,
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a judge evaluating how well someone speaks like a fantasy wizard. You will rate the text on a scale of 1-10, provide brief feedback, and offer specific suggestions for improvement. Respond with a JSON object with fields 'score' (integer 1-10), 'feedback' (string), and 'suggestions' (array of strings)."},
                {"role": "user", "content": f"Evaluate this text for wizard-like qualities: {text}"}
            ],
            max_tokens=500,
            temperature=0.7
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

@app.get("/")
async def root():
    return {"message": "Welcome to the Wizard Trainer API"}

