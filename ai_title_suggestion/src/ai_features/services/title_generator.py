# AI Title Generation Service
# This file will contain the TitleGenerator class for generating blog post titles using Google Gemini API 

import os
import json
import google.generativeai as genai


class TitleGenerator:
    def __init__(self):
        """Initialize the TitleGenerator with Google Gemini API configuration."""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini model: {e}")
    
    def suggest_titles(self, content):
        """
        Generate 3 title suggestions for the given blog post content.
        
        Args:
            content (str): The blog post content to analyze
            
        Returns:
            list: A list of 3 suggested titles as strings
        """
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")
        
        # Build the prompt for Gemini
        prompt = f"""You are a professional blog title generator. Create 3 compelling, clickable blog post titles based on the content below.

Requirements:
- Titles should be 8-12 words long
- Make them engaging and clickable
- Use powerful action words
- Include the main topic/benefit
- NO generic phrases like "Blog Post About" or "Insights on"

Content: {content}

Return ONLY a JSON array with 3 titles, like this format:
["Title 1", "Title 2", "Title 3"]

JSON Array:"""
        
        try:
            # Call the Gemini API
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response - remove markdown formatting
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            # Try to find JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_part = response_text[start_idx:end_idx]
                titles = json.loads(json_part)
            else:
                # Fallback: try parsing the whole response
                titles = json.loads(response_text)
            
            # Validate the response format
            if not isinstance(titles, list):
                raise ValueError("API returned invalid format - not a list")
            
            # Ensure we have exactly 3 titles
            if len(titles) > 3:
                titles = titles[:3]
            elif len(titles) < 3:
                # Pad with generated titles if needed
                while len(titles) < 3:
                    titles.append(f"Generated Title {len(titles) + 1}")
            
            # Ensure all titles are clean strings
            titles = [str(title).strip(' ,"') for title in titles]
            
            return titles
            
        except json.JSONDecodeError:
            # Fallback: try to extract titles from a malformed response
            return self._extract_titles_fallback(response_text)
        except Exception as e:
            # Extract key topics for better fallback titles
            words = content.lower().split()
            key_topics = []
            
            # Look for common important terms
            important_words = ['ai', 'artificial', 'intelligence', 'machine', 'learning', 'technology', 
                             'business', 'marketing', 'social', 'media', 'health', 'routine', 'productivity',
                             'success', 'tips', 'guide', 'strategy', 'future', 'innovation']
            
            for word in words[:20]:  # Check first 20 words
                clean_word = word.strip('.,!?')
                if clean_word in important_words:
                    key_topics.append(clean_word.title())
            
            if not key_topics:
                key_topics = ['Success', 'Guide', 'Tips']
            
            topic = key_topics[0] if key_topics else 'Success'
            
            return [
                f"The Ultimate Guide to {topic} and Growth",
                f"How to Master {topic}: A Complete Strategy",
                f"Transform Your Approach to {topic} Today"
            ]
    
    def _extract_titles_fallback(self, response_text):
        """
        Fallback method to extract titles if JSON parsing fails.
        
        Args:
            response_text (str): The raw response from Gemini
            
        Returns:
            list: A list of 3 fallback titles
        """
        # Try to find lines that look like titles
        lines = response_text.split('\n')
        titles = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and lines that look like JSON artifacts
            if line and not line.startswith('[') and not line.startswith(']'):
                # Remove common prefixes and quotes
                line = line.replace('"', '').replace("'", "")
                if line.startswith('- '):
                    line = line[2:]
                if line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
                    line = line[3:]
                
                if line:
                    titles.append(line)
                    if len(titles) >= 3:
                        break
        
        # Ensure we have exactly 3 titles
        while len(titles) < 3:
            titles.append(f"Blog Post Title {len(titles) + 1}")
        
        return titles[:3] 