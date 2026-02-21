# User Guide: Bible Quiz Automation

This guide explains how to set up, preview, and run the Bible Quiz automation tool.

## 1. Initial Setup

### Prerequisites
- Python 3.10+ installed.
- `credentials.json` placed in the project root (see [Credentials Setup](../setup/google-cloud/CREDENTIALS_SETUP.md)).
- Access to the source Google Sheet.

### Installation
```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the root directory and fill in your spreadsheet details:
```env
SOURCE_SPREADSHEET_ID=your_source_spreadsheet_id_here
SOURCE_SHEET_NAME=03C. Bible Quiz Questions
SOURCE_SHEET_ID=0  # The 'gid' from your sheet URL (usually 0 for the first tab)

# RECOMMENDED: Template Form ID (preserves settings like Manual Release, Verified Email, Progress Bar)
TEMPLATE_FORM_ID=your_template_form_id_here

TAMIL_RESPONSE_SPREADSHEET_ID=your_tamil_response_spreadsheet_id_here
ENGLISH_RESPONSE_SPREADSHEET_ID=your_english_response_spreadsheet_id_here
```

---

## 2. Interactive Web UI (Recommended)

For a more user-friendly experience, you can use the Gradio-based web interface.

```bash
# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Launch the UI
python3 src/interfaces/cli/main.py ui
```

**Features of the Web UI:**
- **Easy Selection:** Choose the week number and language from simple inputs.
- **Tabbed Preview:** Switch between English and Tamil previews with dedicated tabs.
- **Data Tables:** View questions in a structured, searchable table.
- **One-Click Creation:** Click a button to generate forms and get clickable links instantly.

---

## 3. CLI Workflow

### Step 0: The Template Form (One-time Setup)
To automate advanced settings that the Google API doesn't yet support, we use a template:
1. Create a new Google Form manually.
2. Set **Settings > Quizzes > Release grades** to "Later, after manual review".
3. Set **Settings > Responses > Email collection** to "Verified".
4. Set **Settings > Presentation > Show progress bar** to "On".
5. Keep the form **empty** (no questions).
6. Copy the ID from the URL and add it to `TEMPLATE_FORM_ID` in your `.env`.

### Step 1: Preview the Quiz
```bash
# Set PYTHONPATH (run once per terminal session)
export PYTHONPATH=$PYTHONPATH:.

# Preview a specific language (EN or TA)
python3 src/interfaces/cli/main.py preview --week 1 --lang EN

python3 src/interfaces/cli/main.py preview --week 1 --lang TA
```

**What to verify in the preview:**
- **Metadata:** Check the Week number, Date range, and Bible portion.
- **Questions:** Ensure the title follows the `{Q_id}. {Text}` format.
- **Answer Keys:** Ensure the answer key follows the `{Scripture}, {Answer}` format.

### Step 2: Create the Forms
Once you are satisfied with the preview, run the `create` command.

```bash
# Create all languages
python3 src/interfaces/cli/main.py create --week 1

# Create only English
python3 src/interfaces/cli/main.py create --week 1 --lang EN
python3 src/interfaces/cli/main.py create --week 1 --lang TA
```

**Features & Actions:**
1. **Confirmation:** The tool will show the preview again and ask for confirmation.
2. **Unique Titles:** If a form with the same name already exists (e.g., from a previous test), the tool will automatically append a counter: `Week 1 - English Bible Quiz | 2026 (1)`.
3. **Manual Review:** All forms are created with "Later, after manual review" enabled, which also automatically turns on email collection.

### Step 3: Link Responses (Manual)
After the forms are created, you must manually link them to your response spreadsheets:
1. Open the created Form URL.
2. Go to the **Responses** tab.
3. Click **Link to Sheets**.
4. Select your existing response spreadsheet (English or Tamil).
5. The form will automatically create a new tab for this week's responses.

---

## 3. Troubleshooting
- **Authentication Error:** Delete `token.json` and run the command again to re-authenticate.
- **Range Parsing Error:** Ensure `SOURCE_SHEET_NAME` in your `.env` matches the tab name exactly.
- **GID Mismatch:** If the tool cannot find your tab, verify the `SOURCE_SHEET_ID` (the `gid` in the URL).
- **Safari Redirect Issues:** If the browser fails to redirect after login, manually copy the URL printed in the terminal into a different browser.
