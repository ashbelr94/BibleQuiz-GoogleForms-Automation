# PROJECT_CONTEXT: Bible Quiz - Google Forms Automation

This document provides a comprehensive overview of the Bible Quiz Automation project. It serves as the primary entry point for understanding the system's goals, architecture, and current state.

## 1. Project Mission
Automate the weekly creation of Google Forms for Bible quizzes in multiple languages (currently English and Tamil). The tool reads questions and metadata from a master Google Sheet and generates high-quality Google Forms with specific grading and collection settings.

## 2. Core Architecture
The project follows **Clean Architecture** principles to ensure modularity, testability, and future scalability (e.g., adding a Gradio Web UI).

### Layers:
- **Domain (`src/domain/`)**: Pure business logic and data models (Pydantic). No external dependencies.
- **Application (`src/application/`)**: Use cases (Preview, Create) and abstract interfaces (Ports).
- **Infrastructure (`src/infrastructure/`)**: Concrete implementations of Google APIs (Sheets, Forms, Drive) and configuration management.
- **Interfaces (`src/interfaces/`)**: User entry points (CLI using Typer/Rich).

**Detailed Blueprint:** [PYTHON_ARCHITECTURE.md](docs/design/PYTHON_ARCHITECTURE.md)

## 3. The "Template Form" Strategy
Due to current limitations in the **Google Forms API v1** (which doesn't support setting "Manual Grade Release" or "Show Progress Bar" programmatically), this project uses a **Template Copying** workflow:
1. The user creates a manual template form with perfect settings.
2. The script copies this template using the **Drive API**.
3. The script fills the copy with dynamic content using the **Forms API**.

This strategy ensures a 100% automated result that includes settings the API cannot touch.

## 4. Technical Stack
- **Language:** Python 3.10+
- **CLI Framework:** [Typer](https://typer.tiangolo.com/) & [Rich](https://rich.readthedocs.io/)
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Google APIs:** Google Sheets, Google Forms, Google Drive (v3)
- **Settings:** Pydantic-Settings with `.env` support

## 5. Directory Structure
```text
.
├── src/
│   ├── domain/             # Models (Quiz, Question, Metadata)
│   ├── application/        # Use Cases (CreateQuiz, PreviewQuiz)
│   │   └── ports/          # Abstract Interfaces (SheetRepo, FormService)
│   ├── infrastructure/     # Adapters (Google Sheets, Forms, Drive)
│   │   ├── google/         # API Implementations
│   │   └── config/         # Settings Loader
│   └── interfaces/         # Entry Points (CLI)
├── docs/                   # Full Project Documentation
├── English.md / Tamil.md   # Language-specific static description text
└── requirements.txt        # Project dependencies
```

## 6. Data Source & Schema
The tool expects a specific Google Sheet structure identified by its **GID** (usually `0`).
- **Columns:** Q_id, Week, Dates, Portion, Order, Tamil Question, Scripture, Tamil Answer, English Question, English Answer.
- **Formatting:** Questions are formatted as `{Q_id}. {Text}` and answers as `{Scripture}, {Answer}`.

**Detailed Schema:** [SHEET_SCHEMA.md](docs/design/SHEET_SCHEMA.md)

## 7. Current Project Status
- ✅ **Authentication:** OAuth 2.0 flow with broad Drive/Sheets/Forms scopes.
- ✅ **Preview Mode:** Beautiful terminal tables for verifying data before creation.
- ✅ **Create Mode:** Template-based duplication with unique title handling (auto-incrementing counters).
- ✅ **Descriptions:** Dynamic loading of static text from `.md` files with dynamic header replacement.
- 🚧 **Future Scale:** Gradio Web UI implementation plan defined. [UI_ARCHITECTURE.md](docs/design/UI_ARCHITECTURE.md)

## 8. Essential References
- **Setup Guide:** [CREDENTIALS_SETUP.md](docs/setup/google-cloud/CREDENTIALS_SETUP.md)
- **User Guide:** [USAGE.md](docs/user-guide/USAGE.md)
- **Coding Standards:** [PYTHON_BEST_PRACTICES.md](docs/rules/PYTHON_BEST_PRACTICES.md)
- **Implementation History:** [IMPLEMENTATION_PLAN.md](docs/plan/IMPLEMENTATION_PLAN.md)
- **Global Rules:** [GEMINI.md](GEMINI.md)
