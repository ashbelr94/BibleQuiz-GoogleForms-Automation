import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.infrastructure.google.auth import get_google_credentials
from src.infrastructure.google.sheets import GoogleSheetRepository
from src.application.preview_quiz import PreviewQuizUseCase
from src.domain.models import Language

app = typer.Typer(help="Bible Quiz Automation CLI")
console = Console()

@app.command()
def preview(
    week: int = typer.Option(..., help="The week number to preview"),
    lang: Optional[Language] = typer.Option(None, help="Specific language to preview (EN/TA). If omitted, previews all.")
):
    """
    Fetches and displays a preview of the quiz for a given week.
    """
    try:
        # Move credentials fetching outside status to avoid hiding OAuth browser/URL messages
        creds = get_google_credentials()
        
        with console.status(f"[bold blue]Loading data for Week {week}...[/bold blue]"):
            sheet_repo = GoogleSheetRepository(creds)
            use_case = PreviewQuizUseCase(sheet_repo)
            result = use_case.execute(week, language=lang)
        
        if not result:
            console.print(f"[bold red]Error:[/bold red] No data found for Week {week}.")
            raise typer.Exit(code=1)
        
        # Display Metadata
        console.print(Panel(
            f"[bold cyan]Week {result.metadata.week} | {result.metadata.dates} | {result.metadata.portion}[/bold cyan]",
            title="Bible Quiz Metadata",
            border_style="cyan"
        ))
        
        for quiz in result.quizzes:
            lang_name = "English" if quiz.language == Language.ENGLISH else "Tamil"
            
            # Display Description Preview
            console.print(Panel(
                quiz.description,
                title=f"{lang_name} Description Preview",
                border_style="green",
                padding=(1, 2)
            ))
            
            table = Table(title=f"{lang_name} Questions Preview", show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=6)
            table.add_column("Question")
            table.add_column("Answer Key", style="green")
            
            for q in quiz.questions:
                table.add_row(
                    q.id,
                    q.text,
                    q.formatted_answer_key
                )
            
            console.print(table)
            console.print("\n")
            
        console.print("[bold green]Preview successful![/bold green] Run the 'create' command when ready.")

    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

from src.infrastructure.google.forms import GoogleFormService
from src.application.create_quiz import CreateQuizUseCase

@app.command()
def create(
    week: int = typer.Option(..., help="The week number to create forms for"),
    lang: Optional[Language] = typer.Option(None, help="Specific language to create (EN/TA). If omitted, creates all.")
):
    """
    Creates the Google Forms for a given week after user confirmation.
    """
    try:
        # First, show the preview for the selected language(s)
        preview(week, lang=lang)
        
        # Confirmation
        confirm = typer.confirm("\nDo you want to proceed with creating these forms?")
        if not confirm:
            console.print("[bold yellow]Aborted.[/bold yellow]")
            return

        with console.status("[bold green]Creating Google Forms...[/bold green]"):
            creds = get_google_credentials()
            sheet_repo = GoogleSheetRepository(creds)
            form_service = GoogleFormService(creds)
            use_case = CreateQuizUseCase(sheet_repo, form_service)
            
            result = use_case.execute(week, language=lang)
        
        if not result:
            console.print(f"[bold red]Error:[/bold red] Failed to create forms for Week {week}.")
            raise typer.Exit(code=1)
        
        console.print("\n[bold green]Success! Forms created successfully:[/bold green]")
        for l, url in result.created_forms:
            lang_name = "English" if l == Language.ENGLISH else "Tamil"
            console.print(f"  • [bold]{lang_name}:[/bold] {url}")
            
        console.print("\n[yellow]Final Steps (Manual):[/yellow]")
        console.print("  1. Open each form and go to [bold]Settings -> Quizzes[/bold].")
        console.print("  2. Set [bold]Release grades[/bold] to [bold]'Later, after manual review'[/bold].")
        console.print("  3. Go to [bold]Responses[/bold] tab and click [bold]Link to Sheets[/bold] to connect your response spreadsheet.")

    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
