# Bible Quiz - Google Forms Automation

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A robust Python CLI tool designed to automate the weekly creation of multilingual (English & Tamil) Google Forms Bible quizzes. This tool synchronizes directly with a master Google Sheet, extracts questions and metadata, and generates production-ready Google Forms with pre-configured settings.

## 🌟 Features

- **One-Click Generation:** Automates the creation of both English and Tamil quizzes for any specified week.
- **Clean Architecture:** Built with modularity in mind, separating domain logic from external Google API infrastructure.
- **Template-Based Sync:** Preserves advanced Google Form settings (Manual Grade Release, Verified Email, Progress Bar) by copying a master template.
- **Interactive Preview:** Beautiful terminal-based side-by-side translation previews using the `Rich` library.
- **Web UI:** Modern, interactive web interface using `Gradio` for non-technical users.
- **Desktop Mode:** Native Windows standalone window experience with automatic process cleanup.
- **Safe & Robust:** Strict data validation using `Pydantic v2` and secure OAuth 2.0 authentication.
- **Scalable:** Architected to easily support additional languages and future Web UI integration.

## 🛠️ Tech Stack

- **CLI Framework:** Typer
- **UI/Formatting:** Rich
- **Desktop Wrapper:** PyWebView
- **Data Validation:** Pydantic v2
- **Google Cloud APIs:** Sheets, Forms, and Drive (v3)
- **Configuration:** Pydantic-Settings with `.env` support

## 📋 Prerequisites

- Python 3.10+
- A Google Cloud Project with Sheets, Forms, and Drive APIs enabled.
- `credentials.json` from your Google Cloud Console.

## 🚀 Quick Start

### 🏁 Windows Desktop App (Easiest for Non-Technical Users)
If you are on Windows, you don't need to run commands. Just follow these steps:
1.  Ensure you have **Python 3.10+** installed.
2.  Double-click `RunBibleQuiz.bat`.
3.  The app will automatically set up its environment and open in a native window.

### 🐍 CLI / Developer Setup
```bash
# Clone the repository
git clone https://github.com/ashbelr94/BibleQuiz-GoogleForms-Automation.git
cd BibleQuiz-GoogleForms-Automation

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### ⚙️ Configuration
Create a `.env` file in the root directory:
```env
SOURCE_SPREADSHEET_ID=your_id
SOURCE_SHEET_NAME=03C. Bible Quiz Questions
SOURCE_SHEET_ID=0
TEMPLATE_FORM_ID=your_template_id
TAMIL_RESPONSE_SPREADSHEET_ID=your_id
ENGLISH_RESPONSE_SPREADSHEET_ID=your_id
```

### 💻 Command Line Usage
```bash
# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Preview a specific week
python3 src/interfaces/cli/main.py preview --week 1

# Create forms for a specific week
python3 src/interfaces/cli/main.py create --week 1

# Launch the Web UI
python3 src/interfaces/cli/main.py ui
```

## 📖 Documentation

- [Detailed Setup Guide](docs/setup/google-cloud/CREDENTIALS_SETUP.md)
- [User Workflow Guide](docs/user-guide/USAGE.md)
- [Architecture Blueprint](docs/design/PYTHON_ARCHITECTURE.md)
- [Sheet Schema Definition](docs/design/SHEET_SCHEMA.md)

## 👤 Owner
**Ashbel Reinhard**

---
*Developed for spiritual growth and community Bible engagement.*
