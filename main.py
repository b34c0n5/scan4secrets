from core.loader import load_patterns, load_extensions, load_wordlists
from core.scanner import scan_local, scan_remote_file
from core.crawler import crawl_files, normalize_url
from output.reporter import generate_reports
from ui.display import show_summary, show_credits
import argparse
import os
from urllib.parse import urljoin, urlparse
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

results = []

parser = argparse.ArgumentParser(description="Secret Scanner")
parser.add_argument('--path', help='Path to local files')
parser.add_argument('--url', help='Target URL to crawl and scan')
parser.add_argument('--output', default="report", help='Output base filename')
parser.add_argument('--formats', nargs='+', default=["excel"], choices=["excel", "csv", "html", "pdf"], help='Output formats')
args = parser.parse_args()

patterns, pattern_categories = load_patterns()
extensions = load_extensions()
guesses = load_wordlists()

show_summary(patterns, extensions, guesses)
show_credits()

if args.path:
    scan_local(args.path, patterns, pattern_categories, results)

if args.url:
    base_url = normalize_url(args.url)
    domain = urlparse(base_url).netloc
    links = crawl_files(base_url, domain, extensions, wordlist_file="wordlist.txt")

    all_urls = list({urljoin(base_url, guess) for guess in guesses} | links)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Scanning..."),
        BarColumn(),
        TextColumn("[green]{task.completed}/{task.total}"),
        TimeRemainingColumn()
    ) as progress:
        task = progress.add_task("scan", total=len(all_urls))
        for url in all_urls:
            scan_remote_file(url, patterns, pattern_categories, results)
            progress.update(task, advance=1)

if results:
    generate_reports(results, args.output, args.formats)
else:
    print("[INFO] No secrets found.")
