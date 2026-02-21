# Future Scale: Gradio UI Architecture

This document outlines the design and advantages of implementing a web-based UI using **Gradio** for the Bible Quiz Automation tool.

## 1. UI Architecture
Because we followed **Clean Architecture**, the UI will simply be another "Interface" layer that interacts with our existing "Application" layer (Use Cases).

```
src/
├── domain/            # (No changes)
├── application/       # (No changes) - Gradio uses the same Use Cases
├── infrastructure/    # (No changes) - Google API adapters remain the same
└── interfaces/
    ├── cli/           # Current CLI entry point
    └── ui/            # NEW: Gradio UI entry point
        └── app.py     # Gradio interface definition
```

### Data Flow in UI
1.  **User** opens the browser and selects a **Week** from a dropdown.
2.  **Gradio** calls `PreviewQuizUseCase.execute(week)`.
3.  The UI displays a **Dataframe/Table** showing the questions for preview.
4.  **User** clicks a "Create Forms" button.
5.  **Gradio** calls `CreateQuizUseCase.execute(week)`.
6.  The UI displays the generated **Form URLs** as clickable links.

---

## 2. Key Features for the User
A Gradio-based UI would offer several interactive features:

1.  **Week Selection Dropdown:** Instead of typing a number, the user can select from a list of available weeks detected in the Google Sheet.
2.  **Interactive Preview Table:** A rich, searchable table to review English and Tamil questions side-by-side.
3.  **Real-time Validation Alerts:** Visual icons (✅/❌) to indicate if a question is missing an answer or scripture reference before hitting "Create".
4.  **One-Click Creation:** A clear "Generate Forms" button with a loading spinner.
5.  **Clickable Results:** Direct links to the generated Google Forms that open in a new tab.
6.  **Progress Tracking:** A progress bar showing "Reading Sheet...", "Creating English Form...", "Creating Tamil Form...".

---

## 3. Advantages of the Gradio UI
Implementing this UI provides several strategic benefits:

### A. Accessibility for Non-Technical Users
If you ever delegate the weekly quiz creation to someone else who isn't comfortable with a terminal or Python, they can use the web interface without knowing any "code."

### B. Visual Verification
The CLI is great, but a web UI allows for better side-by-side comparison of Tamil and English translations. Seeing them in a structured grid makes it much easier to spot typos or formatting errors.

### C. Zero-Installation (Sharing)
Gradio allows you to generate a **public sharing link** (valid for 72 hours) or host it on a small server. This means you could even run the automation from your phone or tablet by visiting the URL.

### D. Error Resilience
The UI can provide more descriptive "pop-up" error messages if the Google Sheet is shared with the wrong permissions or if a network error occurs.

### E. Extensibility (Editing)
In a future version, the Gradio UI could allow you to **edit** a question directly in the browser *before* it gets sent to Google Forms, providing a final layer of control without needing to go back and forth to the Spreadsheet.

---

## 4. Implementation Sketch (Pseudo-code)
```python
import gradio as gr
from src.application.preview_quiz import PreviewQuizUseCase
from src.application.create_quiz import CreateQuizUseCase

def ui_preview(week):
    result = preview_use_case.execute(week)
    return result.to_dataframe() # Simplified

def ui_create(week):
    result = create_use_case.execute(week)
    return result.english_url, result.tamil_url

with gr.Blocks() as demo:
    week_input = gr.Number(label="Select Week")
    preview_btn = gr.Button("Preview Questions")
    table = gr.Dataframe()
    create_btn = gr.Button("Generate Google Forms", variant="primary")
    links = gr.Markdown()
    
    preview_btn.click(ui_preview, inputs=[week_input], outputs=[table])
    create_btn.click(ui_create, inputs=[week_input], outputs=[links])

demo.launch()
```
