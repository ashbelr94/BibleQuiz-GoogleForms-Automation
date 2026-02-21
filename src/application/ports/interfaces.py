from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Language, Question, QuizMetadata, Quiz

class SheetRepository(ABC):
    """Interface for reading quiz data from a spreadsheet."""
    
    @abstractmethod
    def get_quiz_metadata(self, week: int) -> Optional[QuizMetadata]:
        """Fetches metadata (dates, portion) for a specific week."""
        pass

    @abstractmethod
    def get_questions(self, week: int, language: Language) -> List[Question]:
        """Fetches all questions for a specific week and language."""
        pass

class FormService(ABC):
    """Interface for creating and managing Google Forms."""
    
    @abstractmethod
    def create_form(self, quiz: Quiz) -> str:
        """Creates a Google Form from a Quiz object.
        
        Returns:
            str: The URL of the created form.
        """
        pass

    @abstractmethod
    def link_responses(self, form_id: str, spreadsheet_id: str) -> None:
        """Links the form to a specific response spreadsheet."""
        pass
