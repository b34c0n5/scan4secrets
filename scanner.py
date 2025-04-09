import os
import re
import json
import pandas as pd
import argparse
from fpdf import FPDF
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load patterns from patterns.json
with open("patterns.json", "r") as f:
    raw_patterns = json.load(f)

# Flatten patterns and track categories
patterns = []
pattern_categories = {}
for category, keys in raw_patterns.items():
    for key in keys:
        patterns.append(key)
        pattern_categories[key] = category

print(Fore.CYAN + f"[DEBUG] Loaded {len(patterns)} patterns across {len(raw_patterns)} categories.\n")

# Regex for detecting secrets
regex = re.compile(
    r'(' + '|'.join(re.escape(p) for p in patterns) + r')\s*[:=]\s*[\'"]?([a-zA-Z0-9_\-\/=+:.]{4,})[\'"]?',
    re.IGNORECASE
)

# CLI argument parser
parser = argparse.ArgumentParser(
    description="🔐 Secret Scanner Tool by M14R41",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '--path',
    required=True,
    help='📂 Root folder path to scan for secrets'
)
parser.add_argument(
    '--output',
    default="report",
    help='📝 Output base filename (no extension)'
)
parser.add_argument(
    '--formats',
    nargs='+',
    default=["excel"],
    choices=["excel", "csv", "html", "pdf"],
    help='📄 Output formats (choose one or more: excel csv html pdf)'
)
args = parser.parse_args()

# Setup paths
root_folder = args.path
output_base = os.path.join(root_folder, args.output)

results = []

# Walk and scan files
for root, dirs, files in os.walk(root_folder):
    for file in files:
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for match in regex.finditer(line):
                        variable = match.group(1)
                        value = match.group(2)
                        category = pattern_categories.get(variable, "Unknown")

                        print(f"{Fore.GREEN}[MATCH]{Style.RESET_ALL} {Fore.MAGENTA}{variable}{Style.RESET_ALL} = {Fore.CYAN}{value}{Style.RESET_ALL} (Line {line_num}) in {filepath}")

                        results.append({
                            "Category": category,
                            "Vulnerability": variable,
                            "Value": value,
                            "LineNumber": line_num,
                            "Line": line.strip(),
                            "Filename": filepath
                        })
        except Exception as e:
            print(Fore.RED + f"[ERROR] Skipped {filepath}: {e}")

# Output results
if results:
    df = pd.DataFrame(results)
    column_order = ["Category", "Vulnerability", "Value", "LineNumber", "Line", "Filename"]
    df = df[column_order]

if "excel" in args.formats:
    df = pd.DataFrame(results)
    df.to_excel(output_base + ".xlsx", index=False)
    print(Fore.YELLOW + f"📘 Excel report saved: {output_base}.xlsx")


    if "csv" in args.formats:
        df.to_csv(output_base + ".csv", index=False)
        print(Fore.YELLOW + f"📄 CSV report saved: {output_base}.csv")

    if "html" in args.formats:
        df.to_html(output_base + ".html", index=False)
        print(Fore.YELLOW + f"🌐 HTML report saved: {output_base}.html")

    if "pdf" in args.formats:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Secret Scanner Report", ln=True, align='C')
        pdf.ln(5)
        for _, row in df.iterrows():
            line = f"{row['Filename']} (Line {row['LineNumber']}): {row['Vulnerability']} = {row['Value']}"
            # Safe encoding for Latin-1
            safe_line = line.encode('latin-1', errors='ignore').decode('latin-1')
            pdf.multi_cell(0, 8, txt=safe_line)
        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(0, 10, "Secret Scanner by M14R41", ln=True, align='C')
        pdf.output(output_base + ".pdf")
        print(Fore.YELLOW + f"📕 PDF report saved: {output_base}.pdf")

    print(Fore.CYAN + "\n✅ Scanning complete.")
else:
    print(Fore.MAGENTA + "No secrets found.")
