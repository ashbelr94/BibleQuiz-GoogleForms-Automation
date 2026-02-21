import os
from typing import List, Optional, Tuple
from pydantic import BaseModel

from src.application.ports.interfaces import SheetRepository
from src.domain.models import Language, Quiz, QuizMetadata

class PreviewResult(BaseModel):
    """Container for the preview data of all languages for a week."""
    metadata: QuizMetadata
    quizzes: List[Quiz]

class PreviewQuizUseCase:
    """Use case to fetch and prepare quiz data for preview."""

    def __init__(self, sheet_repo: SheetRepository):
        self.sheet_repo = sheet_repo

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

    def execute(self, week: int, language: Optional[Language] = None) -> Optional[PreviewResult]:
        """Fetches metadata and questions for specific or all languages for a specific week."""
        metadata = self.sheet_repo.get_quiz_metadata(week)
        if not metadata:
            return None

        # Determine which languages to process
        languages_to_process = [language] if language else [Language.ENGLISH, Language.TAMIL]

        quizzes = []
        for lang in languages_to_process:
            questions = self.sheet_repo.get_questions(week, lang)
            if questions:
                custom_desc = self._get_custom_description(lang, metadata)
                quizzes.append(Quiz(
                    metadata=metadata,
                    language=lang,
                    questions=questions,
                    custom_description=custom_desc
                ))
        
        if not quizzes:
            return None

        return PreviewResult(metadata=metadata, quizzes=quizzes)
