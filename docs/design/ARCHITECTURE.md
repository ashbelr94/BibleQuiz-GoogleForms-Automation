# Bible Quiz Automation Architecture

We are comparing two primary approaches to automate Google Form creation from a Google Sheet.

## Option 1: Google Apps Script (GAS)
A "Native" script that lives inside your Google Sheet.
- **How it works:** You open the Google Sheet, click a custom menu ("Bible Quiz" -> "Generate Forms"), and select the Week number.
- **Pros:**
    - **One-Click UI:** Custom menu in the Sheet. No need to open a terminal.
    - **Native Integration:** Built-in `FormApp` and `SpreadsheetApp`.
    - **No Environment Setup:** Works on any browser.
    - **No Secrets Management:** Handles OAuth internally within the Workspace.
- **Cons:**
    - **Developer Experience:** Harder to test locally (though `clasp` helps).
    - **Version Control:** Requires a tool like `clasp` to sync with Git.

## Option 2: Python CLI (using Google APIs)
A local script that you run from your computer.
- **How it works:** You run `python create_quiz.py --week 8` from your terminal.
- **Pros:**
    - **Developer Experience:** Standard unit testing, IDE support, CI/CD possible.
    - **Expertise:** Matches your familiarity with Python/Unix Shell.
    - **Portability:** Can be integrated into a larger system later.
- **Cons:**
    - **Environment Setup:** Requires Python, `pip install`, and a Google Cloud Project.
    - **Secrets Management:** Requires managing `credentials.json` and `token.json` locally.
    - **UI:** Slightly more manual (opening a terminal vs. clicking a button).

## Recommended Strategy
For a "one-click" workflow that feels like a natural extension of your manual process, **Google Apps Script** is usually the most robust and simplest solution for Google Workspace.

However, since you mentioned scale and robustness, we can build a **Python-based CLI** that you can eventually wrap in a simple **Flask/FastAPI UI** or a **Slack command** if you want to scale to others.

## Google Sheet Schema Recommendation
| Week | Portion | Language | Question | Option A | Option B | ... | Correct Answer | Reference | Date |
|------|---------|----------|----------|----------|----------|-----|----------------|-----------|------|
| 8    | Num 21  | EN       | ...      | ...      | ...     | ... | ...            | ...       | ...  |
| 8    | Num 21  | TA       | ...      | ...      | ...     | ... | ...            | ...       | ...  |

**Better Schema for Scalability:**
- One "Master Sheet" for Portions and Weeks.
- Language-specific sheets (English Questions, Tamil Questions) or a single sheet with a `Language` column.
