from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.title_generator import TitleGenerator


class SuggestTitlesView(APIView):
    """
    API view to generate title suggestions for blog post content.
    """
    
    def post(self, request):
        """
        Handle POST requests to generate title suggestions.
        
        Expected JSON body: {"content": "Your blog post text goes here..."}
        Returns: {"suggestions": ["Title 1", "Title 2", "Title 3"]}
        """
        try:
            # Handle both JSON and form data submissions
            try:
                content = request.data.get('content')
            except Exception as parse_error:
                # If JSON parsing fails, try to get from POST data
                content = request.POST.get('content')
                if not content:
                    return Response(
                        {
                            "error": "Invalid request format. Please send JSON with 'content' field.",
                            "expected_format": "{\"content\": \"your blog post text\"}"
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validate that content is provided
            if not content:
                return Response(
                    {
                        "error": "Content is required",
                        "expected_format": "{\"content\": \"your blog post text\"}"
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate that content is not empty
            if not content.strip():
                return Response(
                    {"error": "Content cannot be empty"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Initialize the TitleGenerator service
            generator = TitleGenerator()
            
            # Call the service to get title suggestions
            suggestions = generator.suggest_titles(content)
            
            # Return the suggestions as JSON response
            return Response(
                {"suggestions": suggestions}, 
                status=status.HTTP_200_OK
            )
            
        except ValueError as e:
            # Handle validation errors from TitleGenerator
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Handle any other unexpected errors
            return Response(
                {"error": "An unexpected error occurred while generating titles"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
