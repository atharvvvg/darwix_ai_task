MVP Build Plan: AI Transcription & Content Service
This plan breaks down the development of the application into minimal, verifiable steps. After completing each task, the application state should be stable and testable.
Phase 1: Project Foundation & Scaffolding
This phase creates the basic project structure and a running, but empty, web server.
Task 1: Initialize Project
Goal: move to project directory
Action:
Navigate into: cd audio_transcription
Task 2: Create Directory and Package Structure
Goal: Establish the complete folder and file structure for the Python source code.
Action: Create the following empty files and directories.
mkdir -p src/api/v1/endpoints
mkdir -p src/core
mkdir -p src/services
touch src/**init**.py
touch src/api/**init**.py
touch src/api/v1/**init**.py
touch src/api/v1/endpoints/**init**.py
touch src/core/**init**.py
touch src/services/**init**.py
touch src/main.py
touch src/api/v1/schemas.py
touch src/api/v1/endpoints/transcription.py
touch src/api/v1/endpoints/suggestions.py
touch src/core/config.py
touch src/services/gemini_service.py

Sh
Task 3: Define Project Dependencies
Goal: Create the requirements.txt file listing all necessary packages.
Action: Create a file named requirements.txt in the project root with the following content:
fastapi
uvicorn[standard]
pydantic
google-generativeai
python-dotenv
python-multipart

Txt
Task 4: Setup Environment Configuration and Git Ignore
Goal: Create templates for environment variables and ensure they are not committed to Git.
Action:
Create a file named .gitignore in the project root with this content:

# Byte-compiled / optimized / DLL files

**pycache**/
_.py[cod]
_$py.class

# Virtual environment

venv/
.venv/

# Environment variables

.env

# IDE / Editor specific

.idea/
.vscode/

Create a file named .env in the project root. This is for local testing and will be ignored by Git.
GEMINI_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"

Ini
Task 5: Create a Minimal "Hello World" FastAPI App
Goal: Create a basic, runnable web server to confirm the setup works.
Action: Add the following code to src/main.py:
from fastapi import FastAPI

app = FastAPI(title="AI Transcription & Content Service")

@app.get("/")
def read_root():
return {"status": "ok", "message": "Welcome to the AI Service!"}

Python
Test: Run uvicorn src.main:app --reload from the root directory. Open http://127.0.0.1:8000 in your browser. You should see the welcome message.
Phase 2: Configuration and Service Layer
This phase sets up secure configuration loading and prepares the service layer that will communicate with the Gemini API.
Task 6: Implement Configuration Loading
Goal: Create a centralized way to load the GEMINI_API_KEY from the .env file.
Action: Add the following code to src/core/config.py:
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()

Python
Test: Add from src.core.config import settings; print(f"Loaded API Key: {settings.GEMINI_API_KEY}") to the bottom of src/main.py and restart the server. You should see your API key printed in the console. Remove the print statement after verifying.
Task 7: Create a Stub for the Gemini Service
Goal: Define the Gemini service module with placeholder functions. This allows the API endpoints to be built without implementing the complex AI logic yet.
Action: Add the following code to src/services/gemini_service.py:
import json

class GeminiService:
async def transcribe_audio_with_diarization(self, audio_file_bytes: bytes, mime_type: str): # Placeholder logic
print(f"Received {len(audio_file_bytes)} bytes of type {mime_type}. Simulating API call.")
return {
"full_transcript": "This is a placeholder transcript from the stubbed service.",
"diarization": [
{"speaker": "Speaker A", "start_time": 0.0, "end_time": 2.5, "transcript": "This is a placeholder transcript..."}
]
}

    async def generate_title_suggestions(self, text: str, count: int):
        # Placeholder logic
        print(f"Received text to generate {count} titles. Simulating API call.")
        return [f"Placeholder Title {i+1}" for i in range(count)]

gemini_service = GeminiService()

Python
Phase 3: Implement Transcription Feature
This phase builds out the first core feature from the data schema up to the final API logic.
Task 8: Define Transcription API Schemas
Goal: Create the Pydantic models for the transcription endpoint's request and response validation.
Action: Add the following code to src/api/v1/schemas.py:
from pydantic import BaseModel
from typing import List

class SpeakerTurn(BaseModel):
speaker: str
start_time: float
end_time: float
transcript: str

class TranscriptionResponse(BaseModel):
full_transcript: str
diarization: List[SpeakerTurn]

Python
Task 9: Create and Wire the Transcription Endpoint
Goal: Define the API endpoint that accepts a file upload and connects it to the stubbed service.
Action: Add the following code to src/api/v1/endpoints/transcription.py:
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.api.v1.schemas import TranscriptionResponse
from src.services.gemini_service import gemini_service

router = APIRouter()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def create_transcription(file: UploadFile = File(...)):
if not file.content_type.startswith("audio/"):
raise HTTPException(
status_code=status.HTTP_400_BAD_REQUEST,
detail="Invalid file type. Please upload an audio file."
)

    audio_bytes = await file.read()

    # Call the stubbed service
    result = await gemini_service.transcribe_audio_with_diarization(
        audio_file_bytes=audio_bytes,
        mime_type=file.content_type
    )
    return result

Python
Task 10: Connect the Transcription Router to the Main App
Goal: Make the new transcription endpoint accessible through the main FastAPI application.
Action: Modify src/main.py to include the new router:
from fastapi import FastAPI
from src.api.v1.endpoints import transcription

app = FastAPI(title="AI Transcription & Content Service")

# Include API v1 routers

app.include_router(transcription.router, prefix="/api/v1", tags=["Transcription"])

@app.get("/")
def read_root():
return {"status": "ok", "message": "Welcome to the AI Service!"}

Python
Test: Restart the server. Go to http://127.0.0.1:8000/docs. You should see the new /api/v1/transcribe endpoint. Try uploading any small file to it; you should receive the hardcoded JSON response from the service stub.
Task 11: Implement the Real Transcription Logic
Goal: Replace the placeholder logic in the Gemini service with a real call to the Gemini 1.5 Pro API.
Action: Update the transcribe_audio_with_diarization method in src/services/gemini_service.py:
import google.generativeai as genai
import json
from src.core.config import settings

# Move class definition up

class GeminiService:
def **init**(self):
genai.configure(api_key=settings.GEMINI_API_KEY)
self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    async def transcribe_audio_with_diarization(self, audio_file_bytes: bytes, mime_type: str):
        audio_file = genai.upload_file(contents=audio_file_bytes, mime_type=mime_type)

        prompt = """
        You are an expert audio transcription and diarization system.
        Transcribe the provided audio file. Identify each distinct speaker and label them sequentially as "Speaker A", "Speaker B", etc.
        Provide the start and end timestamps in seconds for each speaker's segment.
        Your output MUST be a single, valid JSON object and nothing else.
        The JSON object must conform to this exact structure:
        {
            "full_transcript": "The complete transcription of the audio as a single string.",
            "diarization": [
                {
                    "speaker": "Speaker A",
                    "start_time": 0.00,
                    "end_time": 10.52,
                    "transcript": "The text spoken by speaker A in this segment."
                }
            ]
        }
        """

        response = await self.model.generate_content_async([prompt, audio_file])

        # Clean up the response to extract only the JSON part
        try:
            # The API often wraps the JSON in ```json ... ```
            json_text = response.text.strip().lstrip("```json").rstrip("```")
            return json.loads(json_text)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing Gemini response: {e}")
            print(f"Raw response text: {response.text}")
            # Consider raising a specific service exception here
            raise ValueError("Failed to get a valid JSON response from the AI model.")

    # ... keep the placeholder generate_title_suggestions for now ...
    async def generate_title_suggestions(self, text: str, count: int):
        print(f"Received text to generate {count} titles. Simulating API call.")
        return [f"Placeholder Title {i+1}" for i in range(count)]

gemini_service = GeminiService()

Python
Test: Restart the server. Use the /docs UI to upload a real audio file (e.g., a short MP3 or WAV). Verify that you receive a valid, structured JSON response with the actual transcription.
Phase 4: Implement Title Suggestion Feature
This phase builds the second feature, reusing the established patterns.
Task 12: Add Title Suggestion Schemas
Goal: Add the Pydantic models for the title suggestion endpoint.
Action: Append the following models to src/api/v1/schemas.py:

# ... existing models from Task 8 ...

from typing import List, Optional

class TitleSuggestionRequest(BaseModel):
text: str
count: Optional[int] = 5

class TitleSuggestionResponse(BaseModel):
titles: List[str]

Python
Task 13: Create and Wire the Title Suggestion Endpoint
Goal: Define the API endpoint that accepts text and connects it to the stubbed service.
Action: Add the following code to src/api/v1/endpoints/suggestions.py:
from fastapi import APIRouter
from src.api.v1.schemas import TitleSuggestionRequest, TitleSuggestionResponse
from src.services.gemini_service import gemini_service

router = APIRouter()

@router.post("/suggest-titles", response_model=TitleSuggestionResponse)
async def create_title_suggestions(request: TitleSuggestionRequest): # Call the stubbed service
titles = await gemini_service.generate_title_suggestions(
text=request.text,
count=request.count
)
return {"titles": titles}

Python
Task 14: Connect the Suggestion Router to the Main App
Goal: Make the new suggestions endpoint accessible.
Action: Modify src/main.py to include the suggestions router:
from fastapi import FastAPI
from src.api.v1.endpoints import transcription, suggestions # Add suggestions

app = FastAPI(title="AI Transcription & Content Service")

# Include API v1 routers

app.include_router(transcription.router, prefix="/api/v1", tags=["Transcription"])
app.include_router(suggestions.router, prefix="/api/v1", tags=["Content Generation"]) # Add this line

@app.get("/")
def read_root():
return {"status": "ok", "message": "Welcome to the AI Service!"}

Python
Test: Restart the server. Go to http://127.0.0.1:8000/docs. Verify the new /api/v1/suggest-titles endpoint exists and returns the hardcoded placeholder titles when called.
Task 15: Implement the Real Title Suggestion Logic
Goal: Replace the placeholder logic in the Gemini service with a real API call.
Action: Update the generate_title_suggestions method in src/services/gemini_service.py:

# ... inside the GeminiService class ...

async def generate_title_suggestions(self, text: str, count: int):
prompt = f"""
You are an expert copywriter specializing in creating compelling, SEO-friendly blog post titles.
Based on the following text, generate exactly {count} unique title suggestions.
Your output MUST be a single, valid JSON array of strings, and nothing else. Do not include any explanations.
Example: ["Title 1", "Title 2", "Title 3"]

    Text:
    ---
    {text}
    ---
    """

    response = await self.model.generate_content_async(prompt)

    try:
        json_text = response.text.strip().lstrip("```json").rstrip("```")
        return json.loads(json_text)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Raw response text: {response.text}")
        raise ValueError("Failed to get a valid JSON response from the AI model.")

Python
Test: Restart the server. Use the /docs UI to call the /api/v1/suggest-titles endpoint with a block of text. Verify you get a real list of suggested titles from the Gemini API.
Phase 5: Finalization
Task 16: Create the README file
Goal: Write comprehensive documentation for setting up and using the service.
Action: Create a README.md file in the project root. Populate it with the setup, run instructions, and API endpoint documentation (with curl examples) as detailed in the original architecture document. This is the final step, as all endpoints and functionality are now confirmed.
