# Google Sheet Schema Definition

This reflects the actual structure of the source spreadsheet.

## Sheet: `QuizData` (Source of Truth)

| Column | Name | Description | Example |
|---|---|---|---|
| A | **Q_id** | Unique ID for the question | Q1 |
| B | **Week** | The week number | 1 |
| C | **Dates** | Date range for the quiz | Jan 1-3 |
| D | **Portion** | Bible portion covered | Gen 1-11 |
| E | **Order** | Sequence within the week | 1 |
| F | **Tamil Question** | The question in Tamil | வேதாகமத்தில் கூறப்பட்ட... |
| G | **Scripture (NKJV)** | Biblical reference | Gen 2:8 |
| H | **Tamil Answer** | The answer in Tamil | கிழக்கு |
| I | **English Question (NKJV)** | The question in English | What is the first direction... |
| J | **English Answer** | The answer in English | East |

## Formatting Logic

### 1. Question Title
The question in the Google Form should be formatted as:
`{Q_id}. {Question Text}`

*Example (Tamil):* `Q1. வேதாகமத்தில் கூறப்பட்ட முதல் திசை எது?`
*Example (English):* `Q1. What is the first direction mentioned in the Bible?`

### 2. Answer Key (Correct Answer)
The answer key (short answer) should combine the scripture reference and the answer:
`{Scripture}, {Answer}`

*Example (Tamil):* `Gen 2:8, கிழக்கு`
*Example (English):* `Gen 2:8, East`

### 3. Points
Each question carries **2 points**.

### 4. Form Settings
- **Type:** Quiz (enable "Make this a quiz").
- **Question Type:** Short Answer.
- **Limit:** 1 response per user.
- **Link to Sheet:** Responses must be sent to a specific target spreadsheet for that language.
