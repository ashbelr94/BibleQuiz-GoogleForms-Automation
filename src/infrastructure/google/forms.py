from typing import List, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from src.application.ports.interfaces import FormService
from src.domain.models import Quiz, Question
from src.infrastructure.config.settings import settings

class GoogleFormService(FormService):
    """Implementation of FormService using Google Forms API."""

    def __init__(self, credentials: Credentials):
        self.forms_service = build("forms", "v1", credentials=credentials)
        self.drive_service = build("drive", "v3", credentials=credentials)

    def _get_unique_title(self, base_title: str) -> str:
        """Checks if a form with the title exists and returns a unique one with a counter."""
        current_title = base_title
        counter = 1
        
        while True:
            # Escape single quotes in title for the query
            safe_title = current_title.replace("'", "\\'")
            query = f"name = '{safe_title}' and mimeType = 'application/vnd.google-apps.form' and trashed = false"
            
            results = self.drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            if not results.get('files', []):
                return current_title
            
            current_title = f"{base_title} ({counter})"
            counter += 1

    def create_form(self, quiz: Quiz) -> str:
        """Creates a Google Form from a Quiz object.
        
        Returns:
            str: The URL of the created form.
        """
        # Ensure the title is unique
        unique_title = self._get_unique_title(quiz.title)
        
        form_id = None
        
        # 1. Create or Copy the form
        if settings.TEMPLATE_FORM_ID:
            # Copy from template to preserve settings (Manual Release, Verified Email, etc.)
            copy_body = {'name': unique_title}
            new_file = self.drive_service.files().copy(
                fileId=settings.TEMPLATE_FORM_ID, 
                body=copy_body
            ).execute()
            form_id = new_file['id']
        else:
            # Fallback: Create new form if no template ID is provided
            form_body = {
                "info": {
                    "title": unique_title,
                    "documentTitle": unique_title,
                }
            }
            form = self.forms_service.forms().create(body=form_body).execute()
            form_id = form.get("formId")
        
        # 2. Build update requests (title, description, questions)
        update_requests = {
            "requests": [
                {
                    "updateFormInfo": {
                        "info": {
                            "title": unique_title, # Set the display title
                            "description": quiz.description
                        },
                        "updateMask": "title,description"
                    }
                }
            ]
        }
        
        # If we didn't use a template, we need to turn on Quiz mode and Verified Emails
        if not settings.TEMPLATE_FORM_ID:
            update_requests["requests"].append({
                "updateSettings": {
                    "settings": {
                        "quizSettings": { "isQuiz": True },
                        "emailCollectionType": "VERIFIED"
                    },
                    "updateMask": "quizSettings.isQuiz,emailCollectionType"
                }
            })

        # 3. Add questions (batchUpdate)
        for index, q in enumerate(quiz.questions):
            update_requests["requests"].append({
                "createItem": {
                    "item": {
                        "title": q.formatted_title,
                        "questionItem": {
                            "question": {
                                "required": True,
                                "grading": {
                                    "pointValue": q.points,
                                    "correctAnswers": {
                                        "answers": [{"value": q.formatted_answer_key}]
                                    }
                                },
                                "textQuestion": {} # Short Answer
                            }
                        }
                    },
                    "location": {
                        "index": index
                    }
                }
            })

        self.forms_service.forms().batchUpdate(formId=form_id, body=update_requests).execute()
        
        return f"https://docs.google.com/forms/d/{form_id}/edit"

    def link_responses(self, form_id: str, spreadsheet_id: str) -> None:
        """
        Note: The Google Forms REST API (v1) does not currently support 
        linking a form to a spreadsheet.
        """
        pass
