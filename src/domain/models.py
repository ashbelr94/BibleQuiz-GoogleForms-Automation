from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Language(str, Enum):
    ENGLISH = "EN"
    TAMIL = "TA"

class Question(BaseModel):
    """Represents a single quiz question in a specific language."""
    id: str = Field(..., description="Unique ID for the question (e.g., Q1)")
    week: int
    text: str = Field(..., description="The question text")
    answer: str = Field(..., description="The correct answer text")
    scripture: str = Field(..., description="Scripture reference (e.g., Gen 2:8)")
    points: int = 2

    @property
    def formatted_title(self) -> str:
        """Q1. What is the first direction mentioned in the Bible?"""
        return f"{self.id}. {self.text}"

    @property
    def formatted_answer_key(self) -> str:
        """Gen 2:8, East"""
        return f"{self.scripture}, {self.answer}"

class QuizMetadata(BaseModel):
    """Metadata for the quiz common across all languages for a week."""
    week: int
    dates: str
    portion: str
    year: int = 2026

class Quiz(BaseModel):
    """The full quiz entity for a specific language."""
    metadata: QuizMetadata
    language: Language
    questions: List[Question]
    custom_description: Optional[str] = None
    
    @property
    def title(self) -> str:
        lang_name = "English" if self.language == Language.ENGLISH else "Tamil"
        return f"Week {self.metadata.week} - {lang_name} Bible Quiz | {self.metadata.year}"

    @property
    def description(self) -> str:
        if self.custom_description:
            return self.custom_description
        return f"Week {self.metadata.week} | {self.metadata.dates} | {self.metadata.portion}"
