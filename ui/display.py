from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box
from rich.text import Text

def show_summary(patterns, extensions, guesses):
    console = Console()

    # Summary Table (tight layout)
    summary_table = Table(show_header=True, box=box.SQUARE, pad_edge=False, expand=False)
    summary_table.add_column("Type", style="cyan", no_wrap=True)
    summary_table.add_column("Cnt", justify="right", style="green", width=4)
    summary_table.add_row("Rules", str(len(patterns)))
    summary_table.add_row("Extensions", str(len(extensions)))
    summary_table.add_row("Wordlist Guesses", str(len(guesses)))

    # Credits Table (tight layout)
    credits_table = Table(show_header=True, box=box.SQUARE, pad_edge=False, expand=False)
    credits_table.add_column("Info", style="cyan", no_wrap=True)
    credits_table.add_column("Details", style="green", no_wrap=False)

    Project = Text("github.com/M14R41", style="bold cyan", overflow="fold", no_wrap=False)

    credits_table.add_row("Support", "SAST, DAST")
    credits_table.add_row("Credits", "M14R41")
    credits_table.add_row("GitHub", Project)
    

    # Combine the two tables side by side
    inner_columns = Columns([summary_table, credits_table], expand=False, equal=False, padding=0)

    # Outer panel with minimal width
    combined_panel = Panel(
        inner_columns,
        title="[bold yellow]Config Summary",
        border_style="yellow",
        padding=(0, 1),
        expand=False,
        width=60  # 👈 Shrunk width to better match actual table size
       
    )

    console.print(combined_panel)




def show_credits():
    pass  # already included in show_summary
