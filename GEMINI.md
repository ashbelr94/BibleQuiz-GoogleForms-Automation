# Bible Quiz - Google Forms Automation

## Project-Specific Rules
- **Language:** Python 3.10+
- **Architecture:** Clean Architecture (Domain, Application, Infrastructure, Interface).
- **Type Safety:** Strict type hints (`typing`, `types`) are mandatory. Use `mypy` for checking.
- **Data Validation:** Use `Pydantic` models for all domain entities and data transfer objects (DTOs).
- **CLI UX:** Use `Rich` library for terminal output, tables, and previews.
- **Documentation:** Google-style docstrings for all functions and classes.
- **Testing:** `pytest` for unit and integration tests. Mock external APIs (Google) in tests.

## Contextual Mandates
- **Modularity:** Core logic must be decoupled from the CLI. The `UseCase` layer should be importable by a future Gradio UI without modification.
- **Secrets:** `credentials.json` and `token.json` must be in `.gitignore`. Use environment variables for non-file config.
- **Preview First:** All "write" operations (creating forms) must have a dry-run/preview mode enabled by default.
- **Google Cloud:** Document setup steps in `docs/setup/google-cloud`.
