# Darwix AI - ASSESSMENT

This repository contains the implementation of two AI-powered features as part of a technical assessment:

## 🎯 Assignment Overview

**Feature 1**: Audio Transcription with Speaker Diarization  
**Feature 2**: AI-Powered Blog Post Title Suggestions

Both services leverage Google Gemini AI to provide intelligent content processing capabilities.

## 📁 Project Structure

```
darwix_ai/
├── README.md                    # This file - Main project overview
├── audio_transcription/         # Feature 1: Audio Transcription Service
│   ├── README.md               # Detailed setup and API documentation
│   ├── requirements.txt
│   └── src/                    # FastAPI application
└── ai_title_suggestion/        # Feature 2: Blog Title Suggestion Service
    ├── README.md               # Detailed setup and API documentation
    ├── requirements.txt
    └── src/                    # Django application
```

## 🚀 Services Overview

### 1. Audio Transcription with Diarization

**Technology**: FastAPI + Google Gemini AI  
**Location**: `./audio_transcription/`

- **Upload audio files** (MP3, WAV, M4A) for transcription
- **Speaker diarization** - identifies "who spoke when"
- **Multilingual support** for various languages
- **Structured JSON output** with timestamps and speaker labels

**Quick Start:**

```bash
cd audio_transcription
pip install -r requirements.txt
uvicorn src.main:app --reload
```

📖 **[Full Documentation →](./audio_transcription/README.md)**

### 2. AI Blog Title Suggestions

**Technology**: Django REST Framework + Google Gemini AI  
**Location**: `./ai_title_suggestion/`

- **Intelligent title generation** from blog post content
- **3 title suggestions** per request
- **Django REST Framework** with browsable API
- **Robust error handling** and fallback systems

**Quick Start:**

```bash
cd ai_title_suggestion
pip install -r requirements.txt
python src/manage.py runserver
```

📖 **[Full Documentation →](./ai_title_suggestion/README.md)**

## 🔧 Prerequisites

- **Python 3.8+**
- **Google Gemini API Key** - Get yours at [Google AI Studio](https://aistudio.google.com/)

## ⚡ Quick Demo

### Audio Transcription API

```bash
curl -X POST "http://localhost:8000/api/v1/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.mp3"
```

### Title Suggestion API

```bash
curl -X POST "http://localhost:8000/api/suggest-titles/" \
     -H "Content-Type: application/json" \
     -d '{"content": "Your blog post content here..."}'
```

## 🌟 Key Features

### Audio Transcription Service

- ✅ **Multilingual transcription** support
- ✅ **Speaker diarization** with timestamps
- ✅ **Multiple audio format** support (MP3, WAV, M4A)
- ✅ **FastAPI** with automatic OpenAPI documentation
- ✅ **Structured JSON** responses

### Blog Title Service

- ✅ **AI-powered title generation** using Gemini 1.5 Flash
- ✅ **Django REST Framework** integration
- ✅ **Intelligent fallback system** when AI is unavailable
- ✅ **Browsable API** interface for easy testing
- ✅ **Production-ready** configuration

## 🔗 API Endpoints

| Service             | Endpoint               | Method | Purpose                        |
| ------------------- | ---------------------- | ------ | ------------------------------ |
| Audio Transcription | `/api/v1/transcribe`   | POST   | Upload audio for transcription |
| Audio Transcription | `/docs`                | GET    | Swagger UI documentation       |
| Title Suggestions   | `/api/suggest-titles/` | POST   | Generate blog post titles      |
| Title Suggestions   | `/api/suggest-titles/` | GET    | Browsable API interface        |

## 🛠️ Environment Setup

Both services require a Google Gemini API key. Create `.env` files in each service directory:

```bash
.env.sample provided in both, replace all fields with your keys
```

## 📊 Assessment Deliverables

- ✅ **Codebase**: Complete implementation of both features
- ✅ **Documentation**: Comprehensive READMEs with setup instructions
- ✅ **API Endpoints**: Both transcription and title suggestion endpoints
- ✅ **Code Quality**: Modular, maintainable architecture
- ✅ **AI Integration**: Effective use of AI for both features

## 🎯 Technical Highlights

- **Microservices Architecture**: Each feature is a separate, independently deployable service
- **Different Frameworks**: Demonstrates proficiency with both FastAPI and Django
- **AI Integration**: Smart prompting and error handling for Gemini AI
- **Production Ready**: Proper configuration management, error handling, and documentation
- **RESTful APIs**: Clean, well-documented API interfaces

## 📝 Testing the Services

1. **Start Audio Transcription Service**:

   ```bash
   cd audio_transcription && uvicorn src.main:app --reload
   ```

   Visit: http://localhost:8000/docs

2. **Start Title Suggestion Service**:
   ```bash
   cd ai_title_suggestion && python src/manage.py runserver
   ```
   Visit: http://localhost:8000/api/suggest-titles/

## 🔍 For Detailed Instructions

- **Audio Transcription**: See [`./audio_transcription/README.md`](./audio_transcription/README.md)
- **Title Suggestions**: See [`./ai_title_suggestion/README.md`](./ai_title_suggestion/README.md)

It was genuinely a fun assessment, thank you! :)

# Darwix AI - ASSESSMENT

This repository contains the implementation of two AI-powered features as part of a technical assessment:

## 🎯 Assignment Overview

**Feature 1**: Audio Transcription with Speaker Diarization  
**Feature 2**: AI-Powered Blog Post Title Suggestions

Both services leverage Google Gemini AI to provide intelligent content processing capabilities.

## 📁 Project Structure

```
darwix_ai/
├── README.md                    # This file - Main project overview
├── audio_transcription/         # Feature 1: Audio Transcription Service
│   ├── README.md               # Detailed setup and API documentation
│   ├── requirements.txt
│   └── src/                    # FastAPI application
└── ai_title_suggestion/        # Feature 2: Blog Title Suggestion Service
    ├── README.md               # Detailed setup and API documentation
    ├── requirements.txt
    └── src/                    # Django application
```

## 🚀 Services Overview

### 1. Audio Transcription with Diarization

**Technology**: FastAPI + Google Gemini AI  
**Location**: `./audio_transcription/`

- **Upload audio files** (MP3, WAV, M4A) for transcription
- **Speaker diarization** - identifies "who spoke when"
- **Multilingual support** for various languages
- **Structured JSON output** with timestamps and speaker labels

**Quick Start:**

```bash
cd audio_transcription
pip install -r requirements.txt
uvicorn src.main:app --reload
```

📖 **[Full Documentation →](./audio_transcription/README.md)**

### 2. AI Blog Title Suggestions

**Technology**: Django REST Framework + Google Gemini AI  
**Location**: `./ai_title_suggestion/`

- **Intelligent title generation** from blog post content
- **3 title suggestions** per request
- **Django REST Framework** with browsable API
- **Robust error handling** and fallback systems

**Quick Start:**

```bash
cd ai_title_suggestion
pip install -r requirements.txt
python src/manage.py runserver
```

📖 **[Full Documentation →](./ai_title_suggestion/README.md)**

## 🔧 Prerequisites

- **Python 3.8+**
- **Google Gemini API Key** - Get yours at [Google AI Studio](https://aistudio.google.com/)

## ⚡ Quick Demo

### Audio Transcription API

```bash
curl -X POST "http://localhost:8000/api/v1/transcribe" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.mp3"
```

### Title Suggestion API

```bash
curl -X POST "http://localhost:8000/api/suggest-titles/" \
     -H "Content-Type: application/json" \
     -d '{"content": "Your blog post content here..."}'
```

## 🌟 Key Features

### Audio Transcription Service

- ✅ **Multilingual transcription** support
- ✅ **Speaker diarization** with timestamps
- ✅ **Multiple audio format** support (MP3, WAV, M4A)
- ✅ **FastAPI** with automatic OpenAPI documentation
- ✅ **Structured JSON** responses

### Blog Title Service

- ✅ **AI-powered title generation** using Gemini 1.5 Flash
- ✅ **Django REST Framework** integration
- ✅ **Intelligent fallback system** when AI is unavailable
- ✅ **Browsable API** interface for easy testing
- ✅ **Production-ready** configuration

## 🔗 API Endpoints

| Service             | Endpoint               | Method | Purpose                        |
| ------------------- | ---------------------- | ------ | ------------------------------ |
| Audio Transcription | `/api/v1/transcribe`   | POST   | Upload audio for transcription |
| Audio Transcription | `/docs`                | GET    | Swagger UI documentation       |
| Title Suggestions   | `/api/suggest-titles/` | POST   | Generate blog post titles      |
| Title Suggestions   | `/api/suggest-titles/` | GET    | Browsable API interface        |

## 🛠️ Environment Setup

Both services require a Google Gemini API key. Create `.env` files in each service directory:

```bash
.env.sample provided in both, replace all fields with your keys
```

## 📊 Assessment Deliverables

- ✅ **Codebase**: Complete implementation of both features
- ✅ **Documentation**: Comprehensive READMEs with setup instructions
- ✅ **API Endpoints**: Both transcription and title suggestion endpoints
- ✅ **Code Quality**: Modular, maintainable architecture
- ✅ **AI Integration**: Effective use of AI for both features

## 🎯 Technical Highlights

- **Microservices Architecture**: Each feature is a separate, independently deployable service
- **Different Frameworks**: Demonstrates proficiency with both FastAPI and Django
- **AI Integration**: Smart prompting and error handling for Gemini AI
- **Production Ready**: Proper configuration management, error handling, and documentation
- **RESTful APIs**: Clean, well-documented API interfaces

## 📝 Testing the Services

1. **Start Audio Transcription Service**:

   ```bash
   cd audio_transcription && uvicorn src.main:app --reload
   ```

   Visit: http://localhost:8000/docs

2. **Start Title Suggestion Service**:
   ```bash
   cd ai_title_suggestion && python src/manage.py runserver
   ```
   Visit: http://localhost:8000/api/suggest-titles/

## 🔍 For Detailed Instructions

- **Audio Transcription**: See [`./audio_transcription/README.md`](./audio_transcription/README.md)
- **Title Suggestions**: See [`./ai_title_suggestion/README.md`](./ai_title_suggestion/README.md)

It was genuinely a fun assessment, thank you! :)

---
