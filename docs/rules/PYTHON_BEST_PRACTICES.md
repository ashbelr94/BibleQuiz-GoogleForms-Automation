# Python Coding Standards & Best Practices

This document defines the coding standards for the Bible Quiz Automation project.

## 1. Code Style
- **Formatting:** Follow PEP 8.
- **Line Length:** 100 characters.
- **Imports:** Group imports: Standard Library, Third Party, Local Application. Use absolute imports.

## 2. Type Hinting
- **Strict Typing:** All function arguments and return values must be type-hinted.
- **Generics:** Use `typing.List`, `typing.Dict`, `typing.Optional` (or built-in `list`, `dict` for Python 3.9+).
- **Checking:** Code should pass `mypy` static analysis.

```python
# GOOD
def get_user_name(user_id: int) -> Optional[str]:
    ...

# BAD
def get_user_name(user_id):
    ...
```

## 3. Data Validation (Pydantic)
- Use **Pydantic** models for all data structures, especially those crossing boundaries (e.g., from Sheet to Domain).
- Define clear constraints (e.g., `min_length=1`).

```python
from pydantic import BaseModel, Field

class Question(BaseModel):
    id: str = Field(..., pattern=r"^Q\d+$")
    text: str
    points: int = 2
```

## 4. Error Handling
- Use **Custom Exceptions** in the Domain layer (`src/domain/exceptions.py`).
- Catch low-level exceptions (like `googleapiclient.errors.HttpError`) in the Infrastructure layer and wrap them in Domain exceptions.
- The CLI layer should catch Domain exceptions and print user-friendly messages using `Rich`.

## 5. Rich CLI Output
- Use `rich.console.Console` for printing.
- Use `rich.table.Table` for lists of data.
- Use `rich.prompt.Prompt` for user input.

```python
from rich.console import Console
console = Console()

console.print("[bold green]Success![/bold green] Form created.")
```

## 6. Testing
- Use `pytest`.
- **Unit Tests:** Test Domain logic and Use Cases. Mock Infrastructure interfaces.
- **Integration Tests:** Test the Google API integration (carefully, using a test sheet).

## 7. Documentation
- Use Google-style docstrings.

```python
def create_quiz(week: int) -> str:
    """Creates a Google Form for the specified week.

    Args:
        week (int): The week number to generate.

    Returns:
        str: The URL of the created form.
    """
```
