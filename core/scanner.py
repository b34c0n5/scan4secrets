import re
import requests
import json
import os
from colorama import Fore, Style

FALSE_POSITIVES = [
    r"\$_POST\[[^\]]*\]\s*=\s*['\"]?[a-zA-Z0-9_]+['\"]?",
    r"csrf_token\s*=",
    r"password\s*=\s*['\"]?(YES|NO)['\"]?",
]

def is_false_positive(line):
    return any(re.search(pattern, line, re.IGNORECASE) for pattern in FALSE_POSITIVES)

def get_category(variable, pattern_categories):
    return pattern_categories.get(variable.lower(), "Unknown")

def print_match(variable, value, line_num, filepath):
    print(
        f"{Fore.GREEN}[MATCH]{Style.RESET_ALL} "
        f"{Fore.LIGHTMAGENTA_EX}{variable:<15}{Style.RESET_ALL} = "
        f"{Fore.CYAN}{value}{Style.RESET_ALL} "
        f"{Fore.YELLOW}(Line {line_num}){Style.RESET_ALL} "
        f"{Fore.WHITE}in {Style.BRIGHT}{filepath}{Style.RESET_ALL}"
    )

def build_regex(patterns, is_web=True):
    pattern_body = '|'.join(re.escape(p) for p in patterns)
    if is_web:
        return re.compile(fr"({pattern_body})\s*[:=]\s*[\'\"]?([\w\-/=+:.!@#$%^&*(){{}}]{{6,}})[\'\"]?", re.IGNORECASE)
    else:
        return re.compile(fr"({pattern_body})\s*[:=]\s*[\'\"]?([\w\-/=+:.]{{4,}})[\'\"]?", re.IGNORECASE)

def scan_remote_file(url, patterns, pattern_categories, results):
    web_regex = build_regex(patterns, is_web=True)
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code not in [200, 301, 302]:
            if resp.status_code == 404:
                print(Fore.RED + "[✘] " + Fore.CYAN + f"{url} " + Fore.MAGENTA + ": Not Found " + Fore.YELLOW + f"(Status {resp.status_code})")

            elif resp.status_code == 403:
                print(Fore.MAGENTA + f"[!] {url} : Forbidden (Status {resp.status_code})")
            else:
                print(Fore.YELLOW + f"[-] {url} : Status {resp.status_code}")
            return
        for line_num, line in enumerate(resp.text.splitlines(), 1):
            if is_false_positive(line):
                continue
            for match in web_regex.finditer(line):
                variable, value = match.groups()
                category = get_category(variable, pattern_categories)
                print_match(variable, value, line_num, url)
                results.append({
                    "Category": category,
                    "Vulnerability": variable,
                    "Value": value,
                    "LineNumber": line_num,
                    "Line": line.strip(),
                    "Filename": url
                })
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Scan interrupted by user.")
        exit(0)  # Or `raise` if you want it to bubble up
        
    except Exception as e:
        print(Fore.RED + f"[ERROR] {url}: {e}")

def scan_local(path, patterns, pattern_categories, results):
    local_regex = build_regex(patterns, is_web=False)
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if is_false_positive(line):
                            continue
                        for match in local_regex.finditer(line):
                            variable, value = match.groups()
                            category = get_category(variable, pattern_categories)
                            print_match(variable, value, line_num, filepath)
                            results.append({
                                "Category": category,
                                "Vulnerability": variable,
                                "Value": value,
                                "LineNumber": line_num,
                                "Line": line.strip(),
                                "Filename": filepath
                            })
            except Exception:
                pass



# ✨ New Integration for Crawling
def scan_content(source_url, content):
    results = []

    CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")
    pattern_path = os.path.join(CONFIG_DIR, "patterns.json")
    with open(pattern_path) as f:
        pattern_map = json.load(f)

    patterns = list(pattern_map.keys())
    categories = {key.lower(): value for key, value in pattern_map.items()}
    regex = build_regex(patterns, is_web=True)

    for line_num, line in enumerate(content.splitlines(), 1):
        if is_false_positive(line):
            continue
        for match in regex.finditer(line):
            variable, value = match.groups()
            category = get_category(variable, categories)
            print_match(variable, value, line_num, source_url)
            results.append({
                "Category": category,
                "Vulnerability": variable,
                "Value": value,
                "LineNumber": line_num,
                "Line": line.strip(),
                "Filename": source_url
            })

    return results



