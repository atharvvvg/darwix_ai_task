# AI Blog Title Suggestion Service

This Django REST API service provides AI-powered blog post title generation using Google Gemini AI. Simply provide your blog post content, and get compelling, clickable titles automatically generated.

## Features

- **AI-Powered Title Generation**: Uses Google Gemini 1.5 Flash model (or whatever model you can afford :P) for intelligent title suggestions
- **Robust Error Handling**: Graceful fallbacks and comprehensive error responses
- **Django REST Framework**: Built with industry-standard Django patterns
- **Production Ready**: Includes proper configuration management and deployment setup

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai_title_suggestion
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
SECRET_KEY="your-super-secret-key-for-django"
DEBUG=True
GEMINI_API_KEY="your-google-gemini-api-key"
```

**To get your Gemini API key:**

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the key and paste it in your `.env` file

### 5. Run Database Migrations

```bash
python src/manage.py migrate
```

## Running the Application

To run the development server:

```bash
python src/manage.py runserver
```

The API will be available at http://127.0.0.1:8000.

Interactive API documentation (Django REST Framework Browsable API) will be available at http://127.0.0.1:8000/api/suggest-titles/.

## API Endpoints

### Blog Post Title Suggestions

**Endpoint:** `POST /api/suggest-titles/`

**Description:** Provide blog post content to receive 3 AI-generated title suggestions.

**Example Request (curl):**

```bash
curl -X POST "http://127.0.0.1:8000/api/suggest-titles/" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
           "content": "Artificial Intelligence is revolutionizing the way businesses operate in 2024. From automated customer service chatbots to predictive analytics that help companies forecast market trends, AI tools are becoming essential for competitive advantage. Machine learning algorithms can now analyze vast amounts of customer data to personalize shopping experiences, while natural language processing enables more intuitive human-computer interactions."
         }'
```

**Request Body Schema:**

```json
{
  "content": "string (required) - The blog post content to generate titles for"
}
```

**Example Success Response (200 OK):**

```json
{
  "suggestions": [
    "Unlock Exponential Growth: How AI is Transforming Business in 2024",
    "Dominate Your Market: Leverage AI for Predictive Analytics and Automated Growth",
    "Future-Proof Your Company: Essential AI Tools for Competitive Advantage"
  ]
}
```

### Using the Django REST Framework Browsable API

1. Navigate to `http://127.0.0.1:8000/api/suggest-titles/`
2. Scroll down to the HTML form section
3. In the **"Content"** field, paste your blog post content
4. Click **POST** to get title suggestions

## Error Handling

### Common Error Responses

**400 Bad Request** - Missing or empty content:

```json
{
  "error": "Content is required",
  "debug_info": "Please provide content in JSON format: {\"content\": \"your blog post text\"}"
}
```

**400 Bad Request** - Invalid JSON format:

```json
{
  "error": "Invalid request format. Please send JSON with 'content' field.",
  "debug_info": "Expected: {\"content\": \"your blog post text\"}",
  "parse_error": "JSON parse error details"
}
```

**500 Internal Server Error** - AI service error:

```json
{
  "error": "An unexpected error occurred while generating titles",
  "debug_error": "Specific error details",
  "debug_type": "ErrorType",
  "debug_traceback": "Full stack trace"
}
```

## Project Structure

```
ai_title_suggestion/
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore file
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── tasks.md                 # Development task list
├── architecture.md          # Project architecture documentation
├── debug_title_generator.py # Debugging utility script
└── src/                     # Main Django application
    ├── manage.py            # Django management script
    ├── core/                # Django project configuration
    │   ├── __init__.py
    │   ├── settings.py      # Django settings with environment variable support
    │   ├── urls.py          # Root URL configuration
    │   ├── wsgi.py          # WSGI configuration
    │   └── asgi.py          # ASGI configuration
    ├── blog/                # Blog application (models)
    │   ├── __init__.py
    │   ├── models.py        # BlogPost model
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── views.py
    │   └── migrations/      # Database migrations
    └── ai_features/         # AI functionality application
        ├── __init__.py
        ├── apps.py
        ├── models.py
        ├── views.py         # SuggestTitlesView API endpoint
        ├── urls.py          # AI features URL configuration
        ├── tests.py
        ├── migrations/
        └── services/        # Business logic layer
            ├── __init__.py
            └── title_generator.py  # TitleGenerator service class
```

## Dependencies

- **Django (~5.0)**: Web framework
- **Django REST Framework (~3.15)**: API framework
- **python-dotenv (~1.0)**: Environment variable management
- **google-generativeai (~0.5.0)**: Google Gemini AI integration
- **gunicorn (~22.0)**: Production WSGI server

## Features in Detail

### AI Title Generation

- **Intelligent Prompting**: Optimized prompts for engaging, clickable titles
- **Fallback System**: Smart fallbacks when API is unavailable
- **Content Analysis**: Extracts key topics for better fallback titles
- **Format Handling**: Robust parsing of AI responses with markdown cleanup

### API Design

- **JSON API**: Clean JSON request/response format
- **Error Handling**: Comprehensive error responses with debugging info
- **Documentation**: Self-documenting with DRF browsable API

## Limitations

- **API Rate Limits**: Subject to Google Gemini API quotas
- **Content Length**: Optimized for typical blog post content (up to ~2000 words)
- **Language**: Primarily optimized for English content
- **Model Dependency**: Requires active Gemini API key

## Further Improvements

- **Caching**: Add Redis caching for frequently requested content
- **Multiple Models**: Support for different AI models (GPT, Claude, etc.)
- **Batch Processing**: Generate titles for multiple posts at once
- **User Management**: Add authentication and user-specific preferences
- **Analytics**: Track popular titles and success metrics
- **A/B Testing**: Support for testing different title variations
