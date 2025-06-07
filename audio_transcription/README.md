# AI Transcription & Content Service

This service provides two main features via a REST API:

- **Audio Transcription with Speaker Diarization**: Transcribes multilingual audio and identifies who spoke when.
- **Blog Post Title Suggestions**: Generates compelling titles from a block of text. (simple extra functionality, thought would be fun)

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd audio_transcription
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project:

```bash
# .env
GEMINI_API_KEY="your-google-api-key-here"
```

**To get your Gemini API key:**

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the key and paste it in your `.env` file

## Running the Application

To run the development server with live reloading:

```bash
uvicorn src.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

Interactive API documentation (Swagger UI) will be available at http://127.0.0.1:8000/docs.

## API Endpoints

### 1. Audio Transcription with Diarization

**Endpoint:** `POST /api/v1/transcribe`

**Description:** Upload an audio file (e.g., MP3, WAV, M4A) to receive a transcription with speaker labels.

**Example Request (curl):**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/transcribe" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio.mp3"
```

**Example Success Response (200 OK):**

```json
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
```

**Supported Audio Formats:**

- MP3 (`audio/mp3`)
- WAV (`audio/wav`)
- M4A (`audio/m4a`)
- And other common audio formats

### 2. Blog Post Title Suggestions

**Endpoint:** `POST /api/v1/suggest-titles`

**Description:** Provide a block of text to generate a list of potential blog post titles.

**Example Request (curl):**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/suggest-titles" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "The latest advancements in AI are transforming industries. From healthcare to finance, machine learning models are optimizing processes and creating new opportunities. This article explores the key trends.",
           "count": 3
         }'
```

**Request Body Schema:**

```json
{
  "text": "string (required) - The text content to generate titles for",
  "count": "integer (optional, default: 5) - Number of titles to generate"
}
```

**Example Success Response (200 OK):**

```json
{
  "titles": [
    "How AI is Revolutionizing Industries: Key Trends to Watch",
    "The Transformative Power of Machine Learning in Finance and Healthcare",
    "Unlocking New Opportunities: A Deep Dive into Modern AI Advancements"
  ]
}
```

## Error Handling

### Common Error Responses

**400 Bad Request** - Invalid file type for transcription:

```json
{
  "detail": "Invalid file type. Please upload an audio file."
}
```

**422 Unprocessable Entity** - Invalid request body:

```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error** - AI service error:

```json
{
  "detail": "Failed to get a valid JSON response from the AI model."
}
```

## Project Structure

```
audio_transcription/
├── .env                  # Environment variables (create this from .env.sample)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── src/                  # Main source code
    ├── __init__.py
    ├── main.py           # FastAPI application entry point
    ├── api/              # API layer
    │   ├── __init__.py
    │   └── v1/           # API version 1
    │       ├── __init__.py
    │       ├── endpoints/
    │       │   ├── __init__.py
    │       │   ├── transcription.py    # Transcription endpoint
    │       │   └── suggestions.py      # Title suggestions endpoint
    │       └── schemas.py              # Pydantic models
    ├── core/             # Core application logic
    │   ├── __init__.py
    │   └── config.py     # Configuration management
    └── services/         # Business logic and external services
        ├── __init__.py
        └── gemini_service.py # Gemini API integration
```

## Deployment

This service is designed to be deployed on any platform that supports Python web applications:

- **Docker**: Create a Dockerfile for containerized deployment
- **Cloud Platforms**: Deploy to Google Cloud Run, AWS Lambda, Heroku, etc.
- **Traditional Servers**: Use gunicorn or uvicorn for production deployment

## Limitations

- Maximum file size for audio transcription: Depends on your deployment configuration
- API rate limits: Subject to Google Gemini API quotas
- Supported languages: Multilingual support provided by Gemini AI

## Further Improvements

- Use latest Gemini models (I could only use Gemini-1.5-flash as it is free) or even better, Google's own STT V2.
- Use services such as ElevenLabs (https://elevenlabs.io/speech-to-text) which specialize in Speech to text.
