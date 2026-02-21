import os
from typing import List, Optional, Tuple
from pydantic import BaseModel

from src.application.ports.interfaces import SheetRepository, FormService
from src.domain.models import Language, Quiz, QuizMetadata

class CreateQuizResult(BaseModel):
    """Container for the results of creating all language forms for a week."""
    metadata: QuizMetadata
    created_forms: List[Tuple[Language, str]] # (Language, Form URL)

class CreateQuizUseCase:
    """Use case to fetch quiz data and create actual Google Forms."""

    def __init__(self, sheet_repo: SheetRepository, form_service: FormService):
        self.sheet_repo = sheet_repo
        self.form_service = form_service

    def _get_custom_description(self, lang: Language, metadata: QuizMetadata) -> Optional[str]:
        """Loads and formats the language-specific description from .md files."""
        file_name = "English.md" if lang == Language.ENGLISH else "Tamil.md"
        if not os.path.exists(file_name):
            return None
            
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if not lines:
            return None
            
        # The first line is replaced by our dynamic metadata
        dynamic_header = f"Week {metadata.week} | {metadata.dates} | {metadata.portion}"
        # Skip the first line and join the rest
        body = "".join(lines[1:]).strip()
        
        return f"{dynamic_header}\n\n{body}"

    def execute(self, week: int, language: Optional[Language] = None) -> Optional[CreateQuizResult]:
        """Fetches metadata and questions, then creates forms for specific or all languages."""
        metadata = self.sheet_repo.get_quiz_metadata(week)
        if not metadata:
            return None

        # Determine which languages to process
        languages_to_process = [language] if language else [Language.ENGLISH, Language.TAMIL]

        created_forms = []
        for lang in languages_to_process:
            questions = self.sheet_repo.get_questions(week, lang)
            if questions:
                custom_desc = self._get_custom_description(lang, metadata)
                quiz = Quiz(
                    metadata=metadata,
                    language=lang,
                    questions=questions,
                    custom_description=custom_desc
                )
                form_url = self.form_service.create_form(quiz)
                created_forms.append((lang, form_url))
        
        if not created_forms:
            return None

        return CreateQuizResult(metadata=metadata, created_forms=created_forms)
