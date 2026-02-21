# Bible Quiz Automation - Implementation Plan

This plan outlines the steps to build the Python CLI for automating Google Forms creation.

## Phase 1: Setup & Infrastructure
**Goal:** Establish the project structure and authenticate with Google.

1.  **Project Initialization:**
    -   Create directory structure (`src/`, `tests/`).
    -   Create `requirements.txt` (typer, rich, pydantic, google-api-python-client, google-auth-httplib2, google-auth-oauthlib).
    -   Create `.gitignore` (ignore `credentials.json`, `token.json`, `venv/`, `__pycache__`).

2.  **Google Cloud Project Setup:**
    -   Create a new Google Cloud Project.
    -   Enable **Google Sheets API**, **Google Drive API**, and **Google Forms API**.
    -   Create OAuth 2.0 Client ID credentials (`credentials.json`).
    -   **Action Item:** User must download `credentials.json` and place it in the project root.

3.  **Authentication Module:**
    -   Implement `src/infrastructure/google/auth.py`.
    -   Handle OAuth flow using `InstalledAppFlow`.
    -   Save/Load `token.json` automatically.

## Phase 2: Domain & Application Core
**Goal:** Define the data models and business logic without external dependencies.

4.  **Domain Models:**
    -   Implement `src/domain/models.py`:
        -   `Question` (id, text, answer, reference, etc.)
        -   `Quiz` (title, description, questions list)
        -   `Config` (spreadsheet IDs)

5.  **Application Interfaces (Ports):**
    -   Define `src/application/ports/sheet_repository.py` (ABC).
    -   Define `src/application/ports/form_service.py` (ABC).

## Phase 3: Google Sheets Integration
**Goal:** Read questions from the Google Sheet.

6.  **Sheet Repository Implementation:**
    -   Implement `src/infrastructure/google/sheets.py`.
    -   Use `googleapiclient` to read the specific range/columns.
    -   Map raw row data to `Question` domain models.
    -   Handle empty rows or missing data gracefully.

7.  **Preview Use Case:**
    -   Implement `src/application/preview_quiz.py`.
    -   Orchestrate reading from the repository.

## Phase 4: CLI Interface & Preview
**Goal:** Allow the user to see what *will* happen.

8.  **CLI Skeleton:**
    -   Implement `src/interfaces/cli/main.py` using `Typer`.
    -   Add `preview` command.

9.  **Rich Integration:**
    -   Use `rich.table.Table` to display the fetched questions nicely in the terminal.
    -   Show warnings if data looks incorrect (e.g., missing answer).

## Phase 5: Google Forms Integration
**Goal:** Create the actual form.

10. **Form Service Implementation:**
    -   Implement `src/infrastructure/google/forms.py`.
    -   Use `forms.create` to make a new form.
    -   Use `forms.batchUpdate` to add items (questions).
        -   **Challenge:** Mapping "Short Answer" correctness.
        -   **Workaround:** Set point value and feedback text. Form API support for text validation is limited but we'll implement what's available.
    -   Use `forms.update` (or similar) to set destination spreadsheet.

11. **Create Use Case:**
    -   Implement `src/application/create_quiz.py`.
    -   Call `Preview` logic first (optional), then `FormService.create`.

## Phase 6: Polish & Documentation
**Goal:** make it production-ready.

12. **Configuration Management:**
    -   Use `.env` or `config.yaml` for Spreadsheet IDs.

13. **Final Testing:**
    -   Run end-to-end test with a real sheet.

14. **Documentation:**
    -   Update `README.md`.
    -   Create `USAGE.md`.
