from fpdf import FPDF
import os
from rich.console import Console
from rich.table import Table
import pandas as pd

def generate_reports(results, output, formats):
    console = Console()

    # Create DataFrame from results
    df = pd.DataFrame(results)
    df = df[["Category", "Vulnerability", "Value", "LineNumber", "Line", "Filename"]]

    # Generate summary table
    summary = Table(title="[bold green]Scan Summary")
    summary.add_column("Category", style="cyan")
    summary.add_column("Count", justify="right", style="green")

    for cat, group in df.groupby("Category"):
        summary.add_row(cat, str(len(group)))
    
    console.print(summary)

    # Loop over the requested formats
    for fmt in formats:
        if fmt == "excel":
            path = os.path.abspath(f"{output}.xlsx")  # Explicitly setting the .xlsx extension for Excel
            try:
                df.to_excel(path, index=False, engine="openpyxl")
                print(f"[+] EXCEL saved to: {path}")
            except Exception as e:
                print(f"[ERROR] Failed to save Excel report: {e}")
        elif fmt == "csv":
            path = os.path.abspath(f"{output}.csv")
            try:
                df.to_csv(path, index=False)
                print(f"[+] CSV saved to: {path}")
            except Exception as e:
                print(f"[ERROR] Failed to save CSV report: {e}")
        elif fmt == "html":
            path = os.path.abspath(f"{output}.html")
            try:
                df.to_html(path, index=False)
                print(f"[+] HTML saved to: {path}")
            except Exception as e:
                print(f"[ERROR] Failed to save HTML report: {e}")
        elif fmt == "pdf":
            path = os.path.abspath(f"{output}.pdf")
            try:
                # Create PDF report
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Scan Results", ln=True, align="C")
                pdf.ln(10)
                for _, row in df.iterrows():
                    pdf.multi_cell(200, 10, f"{row['Category']} - {row['Vulnerability']} : {row['Value']}")
                pdf.output(path)
                print(f"[+] PDF saved to: {path}")
            except Exception as e:
                print(f"[ERROR] Failed to save PDF report: {e}")
