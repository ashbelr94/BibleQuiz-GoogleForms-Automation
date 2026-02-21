from typing import List, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from src.application.ports.interfaces import SheetRepository
from src.domain.models import Language, Question, QuizMetadata
from src.infrastructure.config.settings import settings

class GoogleSheetRepository(SheetRepository):
    """Implementation of SheetRepository using Google Sheets API."""

    def __init__(self, credentials: Credentials):
        self.service = build("sheets", "v4", credentials=credentials)
        self.spreadsheet_id = settings.SOURCE_SPREADSHEET_ID
        self._cached_sheet_name: Optional[str] = None

    def _get_sheet_name_by_id(self, sheet_id: int) -> str:
        """Finds the current title of a sheet by its GID (sheetId)."""
        if self._cached_sheet_name:
            return self._cached_sheet_name

        spreadsheet = self.service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id,
            fields="sheets(properties(title,sheetId))"
        ).execute()

        for sheet in spreadsheet.get('sheets', []):
            if sheet['properties']['sheetId'] == sheet_id:
                self._cached_sheet_name = sheet['properties']['title']
                return self._cached_sheet_name
        
        # Fallback to config if ID not found
        return settings.SOURCE_SHEET_NAME

    def _get_all_rows(self) -> List[List]:
        """Fetches all rows from the spreadsheet using the most reliable sheet title."""
        # Use GID if provided, otherwise fallback to the configured name
        sheet_name = self._get_sheet_name_by_id(settings.SOURCE_SHEET_ID) if settings.SOURCE_SHEET_ID is not None else settings.SOURCE_SHEET_NAME
        
        # Wrap sheet name in single quotes to handle spaces and special characters
        range_name = f"'{sheet_name}'!A:J"
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result.get("values", [])

    def get_quiz_metadata(self, week: int) -> Optional[QuizMetadata]:
        rows = self._get_all_rows()
        if not rows or len(rows) < 2:
            return None
        
        # Skip header, find the first row matching the week
        for row in rows[1:]:
            if len(row) > 1 and str(row[1]) == str(week):
                return QuizMetadata(
                    week=int(row[1]),
                    dates=row[2],
                    portion=row[3],
                    year=settings.QUIZ_YEAR
                )
        return None

    def get_questions(self, week: int, language: Language) -> List[Question]:
        rows = self._get_all_rows()
        if not rows or len(rows) < 2:
            return []
        
        questions = []
        for row in rows[1:]:
            # Ensure the row has enough columns and matches the week
            if len(row) >= 10 and str(row[1]) == str(week):
                q_id = str(row[0])
                scripture = str(row[6])
                
                if language == Language.TAMIL:
                    text = str(row[5])
                    answer = str(row[7])
                else:
                    text = str(row[8])
                    answer = str(row[9])
                
                # Basic validation: ensure text/answer is not empty
                if text.strip() and answer.strip():
                    questions.append(Question(
                        id=q_id,
                        week=week,
                        text=text,
                        answer=answer,
                        scripture=scripture,
                        points=settings.DEFAULT_POINTS
                    ))
        
        return questions
