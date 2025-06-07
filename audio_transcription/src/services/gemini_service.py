import google.generativeai as genai
import json
from src.core.config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def transcribe_audio_with_diarization(self, audio_file_bytes: bytes, mime_type: str):
        import base64
        
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

        # Encode audio bytes to base64 for the API
        audio_data = base64.b64encode(audio_file_bytes).decode('utf-8')
        
        # Create the content parts for the API
        contents = [
            prompt,
            {
                "mime_type": mime_type,
                "data": audio_data
            }
        ]

        response = await self.model.generate_content_async(contents)

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

gemini_service = GeminiService() 