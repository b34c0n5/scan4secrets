import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
import warnings
import sys
import json
import os
import re
import time
from requests.exceptions import RequestException

# Suppress all BeautifulSoup-related warnings
warnings.simplefilter("ignore", Warning)

# Initialize colorama
init(autoreset=True)

# Function to normalize URLs (ensure they have 'http' and are well formatted)
def normalize_url(url):
    url = url.strip().replace(" ", "")
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urlparse(url)
    if not parsed.netloc:
        url = f"http://{parsed.path}"
    return url

# Load regex patterns from a configuration file (patterns.json)
def load_patterns(filepath="config/patterns.json"):
    if not os.path.exists(filepath):
        print(Fore.RED + f"[ERROR] Pattern config file not found: {filepath}")
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            regex_patterns = []
            for group in data.values():
                for pattern in group:
                    try:
                        regex_patterns.append(re.compile(pattern, re.IGNORECASE))
                    except re.error as e:
                        print(Fore.RED + f"[ERROR] Invalid regex pattern: {pattern} ({e})")
            return regex_patterns
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to load patterns: {e}")
        return []

# Load valid file extensions from a configuration file (extensions.json)
def load_extensions(filepath="config/extensions.json"):
    if not os.path.exists(filepath):
        print(Fore.RED + f"[ERROR] Extensions config file not found: {filepath}")
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            print(Fore.RED + "[ERROR] extensions.json must be a list like [\".js\", \".php\"]")
            return []
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to load extensions: {e}")
        return []

# Add found file extensions to the wordlist
def add_extensions_to_wordlist(url, extensions, wordlist_file=None):
    if wordlist_file:
        try:
            with open(wordlist_file, "a") as f:
                for ext in extensions:
                    f.write(f"{url}{ext}\n")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Couldn't write to wordlist: {e}")

# Scan the content of a URL for sensitive data using regex patterns
def scan_for_secrets(url, content, filename):
    patterns = load_patterns()
    matches = []
    matched_patterns = set()  # Set to avoid duplicate matches

    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        for pattern in patterns:
            if pattern.search(line):
                match_key = (pattern.pattern, line_num, line.strip())  # Use pattern, line number, and content as a unique key
                if match_key not in matched_patterns:
                    matches.append((pattern.pattern, line_num, line.strip()))
                    matched_patterns.add(match_key)  # Track this specific match

    if matches:
        for match in matches:
            # Limit the printed match to 200 characters
            match_line = match[2][:50]  # Truncate to 200 characters
            print(Fore.GREEN + Style.BRIGHT + "[MATCH] " + Fore.MAGENTA + match[0] + Fore.BLUE + f" = {match_line} " + Fore.YELLOW + f"(Line {match[1]}) in " + Fore.WHITE + url)
        save_scan_results(url, matches, filename)

    return matches

# Save scan results to a file
def save_scan_results(url, matches, filename):
    try:
        with open(filename, 'a') as f:
            for match in matches:
                # Truncate to 200 characters when saving
                match_line = match[2][:200]
                f.write(f"[MATCH] {match[0]} = {match_line} (Line {match[1]}) in {url}\n")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to save results to {filename}: {e}")

# Recursive function to crawl the site, process files, and collect URLs
def crawl_files(base_url, domain, extensions, depth=0, max_depth=3, visited=None, wordlist_file=None, output_file="scan_results.txt"):
    if visited is None:
        visited = set()

    if depth > max_depth or base_url in visited:
        return set()

    print(Fore.YELLOW + "[-] " + Fore.CYAN + Style.BRIGHT + f"{base_url}")

    try:
        resp = requests.get(base_url, timeout=10)
        if resp.status_code not in [200, 301, 302]:
            return set()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", MarkupResemblesLocatorWarning)
            soup = BeautifulSoup(resp.text, "html.parser")

        visited.add(base_url)
        links = set()

        add_extensions_to_wordlist(base_url, extensions, wordlist_file)

        # Scan the file for secrets if it matches any extension
        if any(base_url.lower().endswith(ext) for ext in extensions):
            scan_for_secrets(base_url, resp.text, output_file)

        # Find all links and assets (like scripts, CSS, etc.)
        for tag in soup.find_all(["a", "script", "link"]):
            attr = tag.get("href") or tag.get("src")
            if not attr:
                continue

            full_url = urljoin(base_url, attr)
            parsed = urlparse(full_url)

            if parsed.netloc == domain:
                if any(parsed.path.lower().endswith(ext) for ext in extensions):
                    links.add(full_url)
                if full_url not in visited:
                    links |= crawl_files(full_url, domain, extensions, depth + 1, max_depth, visited, wordlist_file, output_file)

        return links

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[ERROR] Failed to fetch {base_url}: {e}")
        return set()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Scan interrupted by user (Ctrl+C). Exiting gracefully.")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to crawl {base_url}: {e}")
        return set()

# Entry point of the script
if __name__ == "__main__":
    try:
        start_url = normalize_url("https://evil.com")
        domain = urlparse(start_url).netloc
        extensions = load_extensions()

        # Exit if critical files are missing
        if not extensions:
            print(Fore.RED + "[ERROR] No valid extensions found. Exiting.")
            sys.exit(1)

        print(Fore.GREEN + Style.BRIGHT + "\n[INFO] Starting crawl process...\n")
        links_found = crawl_files(start_url, domain, extensions, wordlist_file="wordlist.txt", output_file="scan_results.txt")

        print(Fore.GREEN + Style.BRIGHT + "\n[Finished] Found links:")
        for link in links_found:
            print(Fore.GREEN + Style.BRIGHT + " -", Fore.CYAN + link)

    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Process interrupted by user (Ctrl+C). Exiting.")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Unexpected error: {e}")
        sys.exit(1)
