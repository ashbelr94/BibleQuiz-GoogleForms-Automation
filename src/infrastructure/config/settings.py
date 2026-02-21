import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    SOURCE_SPREADSHEET_ID: str
    SOURCE_SHEET_NAME: str = "QuizData"
    SOURCE_SHEET_ID: Optional[int] = 0
    
    TEMPLATE_FORM_ID: Optional[str] = None # The ID of the form to use as a template
    
    TAMIL_RESPONSE_SPREADSHEET_ID: str
    ENGLISH_RESPONSE_SPREADSHEET_ID: str
    
    DEFAULT_POINTS: int = 2
    QUIZ_YEAR: int = 2026

    class Config:
        env_file = ".env"

settings = Settings()
