Granular Step-by-Step MVP Plan
This plan is focused solely on building the title suggestion feature.
Phase 0: Project Foundation
Task 1: Create Project Structure & requirements.txt
Action: go to the root folder (ai_title_suggestion), then create the src subfolder, and a requirements.txt file in the root.
requirements.txt content:
django~=5.0
djangorestframework~=3.15
python-dotenv~=1.0
google-generativeai~=0.5.0
gunicorn~=22.0
Use code with caution.
Definition of Done: The directory structure and requirements.txt file exist.
Task 2: Setup Virtual Environment & Install Dependencies
Action: Create a virtual environment, activate it, and install packages.
Commands: python3 -m venv venv, source venv/bin/activate, pip install -r requirements.txt.
Definition of Done: pip freeze shows the specified packages are installed.
Task 3: Create .env and .gitignore Files
Action: Create a .gitignore file to exclude venv/, **pycache**/, db.sqlite3, and .env. Create a .env.example file and copy it to .env.
.env.example content:
SECRET_KEY="your-super-secret-key-for-django"
DEBUG=True
GEMINI_API_KEY="your-google-gemini-api-key"
Use code with caution.
Definition of Done: All three files exist. You have populated your actual GEMINI_API_KEY in the .env file.
Task 4: Initialize and Configure Django Project
Action: Run django-admin startproject core src. Then, edit src/core/settings.py to use python-dotenv to load SECRET_KEY and DEBUG from the environment, and add rest_framework to INSTALLED_APPS.
Definition of Done: The command python src/manage.py runserver starts the server without errors.
Phase 1: Core Blog Application
Task 5: Create the blog App & Model
Action: Run python src/manage.py startapp blog src/blog. In src/blog/models.py, define a BlogPost model with title (CharField) and content (TextField) fields.
Definition of Done: The BlogPost model class is defined in the models.py file.
Task 6: Register blog App & Run Migrations
Action: Add 'blog' to INSTALLED_APPS in src/core/settings.py. Then run python src/manage.py makemigrations blog and python src/manage.py migrate.
Definition of Done: The commands execute successfully and a db.sqlite3 file is created.
Phase 2: AI Title Generation Service
Task 7: Create the ai_features App and Service File
Action: Run python src/manage.py startapp ai_features src/ai_features. Create the directory src/ai_features/services/ and an empty **init**.py file inside it. Create the file title_generator.py inside services/.
Definition of Done: The directory src/ai_features/services/ and the file title_generator.py exist.
Task 8: Register the ai_features App
Action: Add 'ai_features' to INSTALLED_APPS in src/core/settings.py.
Definition of Done: The server still runs without errors.
Task 9: Implement the TitleGenerator Service
Action: Populate src/ai_features/services/title_generator.py with the TitleGenerator class that imports os, json, and google.generativeai. The class should have an **init** method to configure the API key and a suggest_titles(self, content) method to build a prompt, call the Gemini API, and parse the JSON response.
Definition of Done: The TitleGenerator class and its methods are written in the file.
Task 10: Test the Service in Isolation
Action: Add a temporary if **name** == '**main**': block to the bottom of title_generator.py to instantiate the class and call suggest_titles with a hardcoded string. Print the result.
Command: python src/ai_features/services/title_generator.py
Definition of Done: The script runs successfully and prints a list of three string titles to the console. The temporary test block can be removed.
Phase 3: API Endpoint
Task 11: Create the API View
Action: In src/ai_features/views.py, create a DRF APIView called SuggestTitlesView. It should have a post method that extracts content from request.data, calls the TitleGenerator service, and returns a DRF Response with the suggestions.
Definition of Done: The SuggestTitlesView class is fully defined.
Task 12: Create and Wire Up API URLs
Action: Create src/ai_features/urls.py and define a path suggest-titles/ pointing to SuggestTitlesView. Then, in src/core/urls.py, include the ai_features.urls under the /api/ path.
Definition of Done: Both urls.py files are updated correctly.
Task 13: Test the Live Endpoint
Action: Run the server (python src/manage.py runserver). Use curl or Postman to send a POST request to http://127.0.0.1:8000/api/suggest-titles/ with a JSON body: {"content": "Your blog post text goes here..."}.
Definition of Done: The server responds with a 200 OK status and a JSON payload like {"suggestions": ["Suggested Title 1", "Suggested Title 2", "Suggested Title 3"]}.
