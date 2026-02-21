# Bible Quiz Automation - Python Architecture

This document outlines the Clean Architecture approach for the Bible Quiz automation tool. The goal is to separate the core business logic (creating quizzes) from the external interfaces (CLI, future Gradio UI) and infrastructure details (Google APIs).

## 1. Directory Structure
We will organize the code into four main layers:

```
src/
├── domain/            # Entities & Business Logic (Pure Python, no external deps)
│   ├── models.py      # Quiz, Question, WeekConfig (Pydantic models)
│   └── exceptions.py  # Custom exceptions
├── application/       # Use Cases (Orchestrates the domain logic)
│   ├── ports/         # Interfaces (ABC) for repositories & services
│   ├── create_quiz.py # The main use case: reads sheet -> creates form
│   └── preview_quiz.py# Use case to just generate the preview data
├── infrastructure/    # External Implementations (Google APIs, File System)
│   ├── google/        # Google API Clients (Sheets, Forms, Drive)
│   │   ├── auth.py    # OAuth handling
│   │   ├── sheets.py  # Implements SheetRepository
│   │   └── forms.py   # Implements FormService
│   └── config/        # Configuration loader (env vars, json)
└── interfaces/        # Entry Points
    ├── cli/           # Command Line Interface (Typer/Click + Rich)
    │   └── main.py    # The CLI entry point
    └── ui/            # Future Gradio UI (Placeholder)
```

## 2. Layer Responsibilities

### Domain Layer
- **Models:** Defines `Question`, `Quiz`, `AnswerKey` using Pydantic.
- **Rules:** e.g., "A quiz cannot have more than 20 questions", "Each question is worth 2 points".
- **Validation:** Ensures `Q_id` format is correct (e.g., "Q1").

### Application Layer
- **Use Cases:** Contains the step-by-step logic.
  - `CreateQuizUseCase`:
    1.  Get `WeekConfig` (week number).
    2.  Call `SheetRepository` to get questions for that week.
    3.  Validate questions.
    4.  (Optional) Call `PreviewService` to show user.
    5.  Call `FormService` to create the form.
    6.  Call `FormService` to link responses to the sheet.
- **Ports:** Defines *interfaces* like `SheetRepository` and `FormService` so the Application layer doesn't depend on concrete Google API implementations. This makes testing easier.

### Infrastructure Layer
- **Google Adapter:** Implements the `SheetRepository` and `FormService` interfaces using `google-api-python-client`.
- **Auth:** Handles `credentials.json` and `token.json`.
- **Config:** Reads spreadsheet IDs from environment variables or a `config.yaml`.

### Interface Layer
- **CLI:**
  - Uses `Typer` for command parsing.
  - Uses `Rich` for beautiful terminal output (tables, progress bars).
  - Calls the Application layer use cases.
- **Gradio UI (Future):**
  - Will simply import the same Use Cases and wrap them in a web UI.

## 3. Data Flow
1.  **User** runs `python main.py create --week 8`.
2.  **CLI** parses arguments and instantiates `CreateQuizUseCase`.
3.  **UseCase** calls `SheetRepository.get_questions(week=8)`.
4.  **SheetRepository** (Infra) calls Google Sheets API, gets rows, maps them to **Domain** `Question` objects.
5.  **UseCase** receives `List[Question]`.
6.  **UseCase** calls `FormService.create_form(quiz)`.
7.  **FormService** (Infra) calls Google Forms API to create the form and add items.
8.  **CLI** displays success message with the form URL.

## 4. Key Technologies
- **Pydantic:** Data validation and settings management.
- **Typer:** Modern CLI builder.
- **Rich:** Terminal formatting (tables, colors).
- **Google Client Library:** Official Python SDK for Google APIs.
- **Pytest:** Testing framework.
