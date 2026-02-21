import gradio as gr
import pandas as pd
from typing import Optional, List, Tuple, Dict, Any

from src.infrastructure.google.auth import get_google_credentials
from src.infrastructure.google.sheets import GoogleSheetRepository
from src.infrastructure.google.forms import GoogleFormService
from src.application.preview_quiz import PreviewQuizUseCase
from src.application.create_quiz import CreateQuizUseCase
from src.domain.models import Language, Quiz

def get_use_cases():
    """Initializes and returns the use cases with necessary adapters."""
    creds = get_google_credentials()
    sheet_repo = GoogleSheetRepository(creds)
    form_service = GoogleFormService(creds)
    
    preview_use_case = PreviewQuizUseCase(sheet_repo)
    create_use_case = CreateQuizUseCase(sheet_repo, form_service)
    
    return preview_use_case, create_use_case

def format_questions_to_df(quiz: Quiz) -> pd.DataFrame:
    """Converts quiz questions to a Pandas DataFrame for display."""
    data = []
    for q in quiz.questions:
        data.append({
            "ID": q.id,
            "Question": q.text,
            "Answer Key": q.formatted_answer_key
        })
    return pd.DataFrame(data)

def handle_preview(week: int, lang_choice: str):
    """Action for the Preview button."""
    try:
        lang = None
        if lang_choice == "English":
            lang = Language.ENGLISH
        elif lang_choice == "Tamil":
            lang = Language.TAMIL
            
        preview_use_case, _ = get_use_cases()
        result = preview_use_case.execute(week, language=lang)
        
        if not result:
            return (
                f"### ❌ Error\nNo data found for Week {week}.",
                "", # Metadata
                pd.DataFrame(), # EN Table
                "", # EN Desc
                pd.DataFrame(), # TA Table
                "", # TA Desc
                0   # Reset last_preview_week
            )
        
        metadata_md = (
            f"### 📅 Week {result.metadata.week}\n"
            f"**Dates:** {result.metadata.dates}  \n"
            f"**Portion:** {result.metadata.portion}"
        )
        
        en_df = pd.DataFrame()
        en_desc = ""
        ta_df = pd.DataFrame()
        ta_desc = ""
        
        for quiz in result.quizzes:
            if quiz.language == Language.ENGLISH:
                en_df = format_questions_to_df(quiz)
                en_desc = quiz.description
            elif quiz.language == Language.TAMIL:
                ta_df = format_questions_to_df(quiz)
                ta_desc = quiz.description
                
        return (
            "### ✅ Preview loaded successfully.",
            metadata_md,
            en_df,
            en_desc,
            ta_df,
            ta_desc,
            week # Update last_preview_week
        )
    except Exception as e:
        return (f"### ❌ Unexpected Error\n{str(e)}", "", pd.DataFrame(), "", pd.DataFrame(), "", 0)

def handle_create_request(week: int, last_preview_week: int, lang_choice: str):
    """Validates week match and performs creation if valid."""
    if week != last_preview_week:
        return (
            f"### ⚠️ Week Mismatch\nYou have changed the week to **{week}**, but the current preview is for Week **{last_preview_week}**.\n\n"
            f"Please click **Preview Quiz Data** for Week {week} first to verify the questions before generating forms."
        )
    
    try:
        lang = None
        if lang_choice == "English":
            lang = Language.ENGLISH
        elif lang_choice == "Tamil":
            lang = Language.TAMIL
            
        _, create_use_case = get_use_cases()
        
        # Show a temporary status if possible, but handle_create_request is a single call
        result = create_use_case.execute(week, language=lang)
        
        if not result:
            return f"### ❌ Error\nFailed to create forms for Week {week}."
        
        output_md = f"### 🎉 Success! Forms created for Week {week}:\n"
        for l, url in result.created_forms:
            lang_name = "English" if l == Language.ENGLISH else "Tamil"
            output_md += f"- **{lang_name}:** [Open Google Form]({url})\n"
            
        output_md += "\n#### ⚠️ Next Steps (Manual):\n"
        output_md += "1. Open each form and go to **Settings -> Quizzes**.\n"
        output_md += "2. Set **Release grades** to **'Later, after manual review'**.\n"
        output_md += "3. Go to **Responses** tab and click **Link to Sheets** to connect your response spreadsheet."
        
        return output_md
    except Exception as e:
        return f"### ❌ Unexpected Error\n{str(e)}"

# Build Gradio UI
with gr.Blocks(title="Bible Quiz Automation", theme=gr.themes.Soft()) as demo:
    # State to track the last week that was successfully previewed
    last_preview_week = gr.State(value=0)

    gr.Markdown("# 📖 Bible Quiz Automation")
    gr.Markdown("Automate the creation of Google Forms for weekly Bible Quizzes.")
    
    with gr.Row():
        with gr.Column(scale=1):
            week_input = gr.Number(label="Week Number", value=1, precision=0)
            lang_input = gr.Radio(
                choices=["All", "English", "Tamil"], 
                label="Language Selection", 
                value="All"
            )
            preview_btn = gr.Button("🔍 1. Preview Quiz Data", variant="secondary")
            create_btn = gr.Button("🚀 2. Generate Google Forms", variant="primary")
            
        with gr.Column(scale=2):
            status_output = gr.Markdown("Ready. Start by selecting a week and clicking Preview.")
            metadata_display = gr.Markdown("")

    with gr.Tabs() as tabs:
        with gr.Tab("English Preview", id=0):
            en_desc_display = gr.Markdown("*Preview not loaded*")
            en_table_display = gr.Dataframe(label="English Questions")
            
        with gr.Tab("Tamil Preview", id=1):
            ta_desc_display = gr.Markdown("*Preview not loaded*")
            ta_table_display = gr.Dataframe(label="Tamil Questions")

    # Wire up the buttons
    preview_btn.click(
        fn=handle_preview,
        inputs=[week_input, lang_input],
        outputs=[status_output, metadata_display, en_table_display, en_desc_display, ta_table_display, ta_desc_display, last_preview_week]
    )
    
    # Combined Validation and Creation
    create_btn.click(
        fn=handle_create_request,
        inputs=[week_input, last_preview_week, lang_input],
        outputs=[status_output]
    )

if __name__ == "__main__":
    demo.launch()
