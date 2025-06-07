```
Architecture: AI Transcription & Content Service
This document outlines the complete architecture for an application that provides audio transcription with speaker diarization and blog post title suggestions, powered by the Google Gemini API.
1. Architecture Overview
The system is designed as a monolithic Python service using the FastAPI web framework. This choice provides high performance, asynchronous capabilities (crucial for I/O-bound tasks like calling external APIs), automatic API documentation, and data validation via Pydantic.
The core logic is centered around interacting with the Google Gemini API. Specifically, we will leverage:
Gemini 1.5 Pro: For the transcription and diarization feature. Its large context window and native audio understanding make it ideal for processing an entire audio file in a single prompt to request a structured JSON output with speaker labels. This also inherently supports multilingual audio.
Gemini 1.0 Pro or 1.5 Pro: For the title suggestion feature, which is a text-in, text-out task.
High-Level Data Flow
Client Request: A user sends an HTTP request to the FastAPI server.
For transcription: A POST request with an audio file (multipart/form-data).
For title suggestions: A POST request with a JSON body containing the text.
FastAPI Server:
Receives and validates the request using Pydantic models.
The relevant API endpoint calls a dedicated Service module.
Service Layer:
The service module encapsulates all interactions with the Google Gemini API.
It constructs a specific prompt tailored for the task (e.g., "Transcribe this audio and identify each speaker with a unique label...").
It sends the audio file or text to the Gemini API using the google-generativeai Python SDK.
Gemini API:
Processes the request.
Returns a structured response (we will prompt it to return JSON).
Response Handling:
The Service Layer parses the response from Gemini.
The API Endpoint validates the outgoing data against a Pydantic response model.
The FastAPI server sends the final, structured JSON response back to the client.
Visual Flow
+-----------+      (1) HTTP Request       +-------------------+      (3) Prompt + Data      +---------------+
|           |   (Audio File / JSON Text)  |                   |--------------------------->|               |
|  Client   |---------------------------->|  FastAPI Server   |                            |  Google Gemini|
|           |                             | (Uvicorn + Python)|      (4) Structured JSON   |      API      |
|           |<----------------------------|                   |<---------------------------|               |
+-----------+      (5) JSON Response      +-------------------+                            +---------------+

2. File and Folder Structure
A modular structure separates concerns, making the codebase easier to navigate, test, and maintain.
/gemini-transcription-service/
├── .env                  # Stores environment variables like the API key
├── .gitignore            # Standard git ignore file
├── README.md             # Project documentation (as requested)
├── requirements.txt      # Python dependencies
└── src/                  # Main source code directory
    ├── __init__.py
    ├── api/              # API layer: endpoints and schemas
    │   ├── __init__.py
    │   └── v1/           # API versioning
    │       ├── __init__.py
    │       ├── endpoints/
    │       │   ├── __init__.py
    │       │   ├── transcription.py    # Endpoint for transcription
    │       │   └── suggestions.py      # Endpoint for title suggestions
    │       └── schemas.py              # Pydantic models for request/response validation
    ├── core/             # Core application logic and configuration
    │   ├── __init__.py
    │   └── config.py     # Configuration management (loads .env)
    ├── main.py           # FastAPI application entry point
    └── services/         # Business logic and external service integrations
        ├── __init__.py
        └── gemini_service.py # Logic for interacting with the Gemini API

3. Component Breakdown (What Each Part Does)
/.env
Stores sensitive information and configuration. It should never be committed to version control.
# .env
GEMINI_API_KEY="your-google-api-key-here"

Ini
/requirements.txt
Lists all Python dependencies for easy installation.
# requirements.txt
fastapi
uvicorn[standard]
pydantic
google-generativeai
python-dotenv
python-multipart

Txt
src/main.py
This is the heart of the web application.
Purpose: Initializes the FastAPI app, loads configuration, and includes the API routers from the api/v1/ directory.
Key Actions:
Create app = FastAPI(...).
Import and use app.include_router(...) for the transcription and suggestion endpoints.
Define a root endpoint (/) for a simple health check.
src/core/config.py
Handles application settings.
Purpose: To load environment variables from the .env file into a strongly-typed settings object.
Key Actions: Uses Pydantic's BaseSettings or a simple os.getenv wrapper to provide configuration (like GEMINI_API_KEY) to the rest of the application. This centralizes configuration.
src/api/v1/schemas.py
Defines the data shape for API inputs and outputs.
Purpose: To ensure all data flowing in and out of the API is valid and structured. This is how we enforce the "structured JSON" requirement.
Example Pydantic Models:
from pydantic import BaseModel
from typing import List, Optional

# For Transcription
class SpeakerTurn(BaseModel):
    speaker: str  # e.g., "Speaker A", "Speaker B"
    start_time: float # in seconds
    end_time: float # in seconds
    transcript: str

class TranscriptionResponse(BaseModel):
    full_transcript: str
    diarization: List[SpeakerTurn]

# For Title Suggestions
class TitleSuggestionRequest(BaseModel):
    text: str
    count: Optional[int] = 5

class TitleSuggestionResponse(BaseModel):
    titles: List[str]

Python
src/api/v1/endpoints/transcription.py
Defines the transcription API endpoint.
Purpose: To handle the HTTP logic for the transcription feature.
Key Actions:
Defines an async POST endpoint, e.g., @router.post("/transcribe", response_model=TranscriptionResponse).
Accepts a file upload (audio: UploadFile = File(...)).
Calls the gemini_service.transcribe_audio_with_diarization() function.
Handles potential errors (e.g., file not provided, API error) and returns appropriate HTTP status codes.
Returns the structured JSON response.
src/api/v1/endpoints/suggestions.py
Defines the title suggestion API endpoint.
Purpose: To handle the HTTP logic for the title suggestion feature.
Key Actions:
Defines an async POST endpoint, e.g., @router.post("/suggest-titles", response_model=TitleSuggestionResponse).
Accepts a JSON body that validates against the TitleSuggestionRequest schema.
Calls the gemini_service.generate_title_suggestions() function.
Returns the list of titles in the TitleSuggestionResponse format.
src/services/gemini_service.py
The most critical module for AI integration.
Purpose: To abstract all communication with the Google Gemini API. The rest of the app doesn't need to know the details of the Gemini SDK.
Key Actions:
Initializes the Gemini client with the API key from core.config.
async def transcribe_audio_with_diarization(audio_file_bytes, mime_type):
Takes the audio file content (bytes) and its MIME type as input.
Uploads the file using the Gemini API's File API if necessary or includes it directly in the prompt for Gemini 1.5.
Constructs a very specific prompt. Example:
"You are an expert audio transcription and diarization system. Transcribe the following audio file. Identify each speaker and label them as 'Speaker A', 'Speaker B', etc. Provide the start and end timestamps for each speaker's turn. Your output MUST be a single, valid JSON object following this exact structure: {"full_transcript": "...", "diarization": [{"speaker": "...", "start_time": ..., "end_time": ..., "transcript": "..."}]}. Do not include any other text or explanations outside of this JSON object."
Calls the model.generate_content() method with the audio and the prompt.
Parses the JSON response from Gemini and returns it as a Python dictionary.
async def generate_title_suggestions(text, count):
Takes the transcribed text as input.
Constructs a prompt. Example:
"You are an expert copywriter. Based on the following text, generate {count} compelling and SEO-friendly blog post titles. Return the result as a JSON array of strings, like ["Title 1", "Title 2"]."
Calls the model, parses the JSON response, and returns a list of strings.
4. State Management and Service Connection
Where State Lives
Application State (Configuration): This state is stateless in a traditional sense but requires configuration. The GEMINI_API_KEY lives in the .env file. It is loaded once on application startup by src/core/config.py and is treated as a constant throughout the application's lifecycle. It is injected into the gemini_service where needed.
Request State: The application is stateless. Each API request is self-contained. The uploaded audio file and request data exist only for the duration of that single request. FastAPI manages this state within the request's context. There is no session management or database needed for this core implementation.
Data Persistence: There is no data persistence. The result of the transcription or title suggestion is generated and immediately returned to the client in the HTTP response. If you needed to handle very long audio files that could cause timeouts, the architecture would need to be extended with a background task queue (like Celery + Redis) and a database (like PostgreSQL) to store job status and results. However, for this requirement, a direct synchronous (from the client's perspective) response is sufficient.
How Services Connect
The connection is managed through a clear, layered dependency flow:
Entrypoint (main.py) -> API Layer (endpoints/*.py): The main.py file acts as the assembler, importing the routers defined in the endpoints. FastAPI handles routing the HTTP request to the correct function in the endpoint file.
API Layer (endpoints/*.py) -> Service Layer (gemini_service.py):
The endpoint function for transcription receives an UploadFile object. It reads the file's bytes (await audio.read()) and passes these bytes, along with the file's content type, to the transcribe_audio_with_diarization function in the gemini_service.
The endpoint function for suggestions passes the text from the request body to the generate_title_suggestions function.
This is a simple function call. The API layer depends on the service layer.
Service Layer (gemini_service.py) -> External API (Google Gemini):
The gemini_service uses the google-generativeai SDK.
It configures the SDK with the API key loaded from core.config.
It makes an async network call to the Gemini API and awaits the response. This is the primary I/O operation.
This layered approach ensures that if you ever wanted to switch from Gemini to another AI provider, you would only need to change the implementation inside src/services/gemini_service.py. The API layer would remain untouched.
5. README.md (Example Structure)
The final README.md in the repository would look like this:
AI Transcription & Content Service
This service provides two main features via a REST API:
Audio Transcription with Speaker Diarization: Transcribes multilingual audio and identifies who spoke when.
Blog Post Title Suggestions: Generates compelling titles from a block of text.
Setup
1. Clone the Repository
git clone <your-repo-url>
cd gemini-transcription-service


2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root of the project by copying the example:
cp .env.example .env

Now, edit the .env file and add your Google Gemini API key:
# .env
GEMINI_API_KEY="your-google-api-key-here"

Running the Application
To run the development server with live reloading:
uvicorn src.main:app --reload

The API will be available at http://127.0.0.1:8000.
Interactive API documentation (Swagger UI) will be available at http://127.0.0.1:8000/docs.
API Endpoints
1. Audio Transcription with Diarization
Endpoint: POST /api/v1/transcribe
Description: Upload an audio file (e.g., MP3, WAV, M4A) to receive a transcription with speaker labels.
Example Request (curl):
curl -X POST "http://127.0.0.1:8000/api/v1/transcribe" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio.mp3"

Example Success Response (200 OK):
{
  "full_transcript": "Hello, this is Speaker A. How are you? I'm doing well, thanks for asking. This is Speaker B.",
  "diarization": [
    {
      "speaker": "Speaker A",
      "start_time": 0.5,
      "end_time": 2.8,
      "transcript": "Hello, this is Speaker A. How are you?"
    },
    {
      "speaker": "Speaker B",
      "start_time": 3.1,
      "end_time": 5.9,
      "transcript": "I'm doing well, thanks for asking. This is Speaker B."
    }
  ]
}

2. Blog Post Title Suggestions
Endpoint: POST /api/v1/suggest-titles
Description: Provide a block of text to generate a list of potential blog post titles.
Example Request (curl):
curl -X POST "http://127.0.0.1:8000/api/v1/suggest-titles" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "The latest advancements in AI are transforming industries. From healthcare to finance, machine learning models are optimizing processes and creating new opportunities. This article explores the key trends.",
           "count": 3
         }'

Example Success Response (200 OK):
{
  "titles": [
    "How AI is Revolutionizing Industries: Key Trends to Watch",
    "The Transformative Power of Machine Learning in Finance and Healthcare",
    "Unlocking New Opportunities: A Deep Dive into Modern AI Advancements"
  ]
}
```