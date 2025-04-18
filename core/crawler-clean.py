import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)

def normalize_url(url):
    """Normalize the URL by adding http:// if missing and stripping extra spaces."""
    url = url.strip().replace(" ", "")
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urlparse(url)
    if not parsed.netloc:
        url = f"http://{parsed.path}"
    return url

def add_extensions_to_wordlist(url, extensions, wordlist_file=None):
    """Add the URLs with extensions to the wordlist if file is provided."""
    if wordlist_file:
        try:
            with open(wordlist_file, "a") as f:
                for ext in extensions:
                    f.write(f"{url}{ext}\n")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Couldn't write to wordlist: {e}")

def scan_for_secrets(url, content):
    """Scan the content of the file for secrets based on some common patterns."""
    patterns = ["password", "token", "apikey", "secret", "auth", "access_key", "db_password"]
    matches = []
    for pattern in patterns:
        if pattern in content.lower():
            matches.append(pattern)
    if matches:
        print(Fore.RED + f"[MATCH] Secrets found in {url}: {', '.join(matches)}")
    return matches

def crawl_files(base_url, domain, extensions, depth=0, max_depth=3, visited=None, wordlist_file=None):
    """Crawl the website and scan for secrets."""
    if visited is None:
        visited = set()
    if depth > max_depth or base_url in visited:
        return set()

    try:
        # Skip fragment-only URLs (e.g., http://m14r41.in#projects)
        if "#" in base_url:
            return set()

        resp = requests.get(base_url, timeout=10)
        if resp.status_code not in [200, 301, 302]:
            return set()

        soup = BeautifulSoup(resp.text, "html.parser")
        links = set()
        visited.add(base_url)

        # Add extensions to wordlist if required
        add_extensions_to_wordlist(base_url, extensions, wordlist_file)

        # Scan the content for secrets if it's a file type we care about
        if any(base_url.lower().endswith(ext) for ext in extensions):
            scan_for_secrets(base_url, resp.text)

        # Process all links in the page
        for tag in soup.find_all(["a", "script", "link"]):
            attr = tag.get("href") or tag.get("src")
            if not attr:
                continue

            full_url = urljoin(base_url, attr)
            parsed = urlparse(full_url)

            # Check if the link is within the same domain
            if parsed.netloc == domain:
                if any(parsed.path.lower().endswith(ext) for ext in extensions):
                    links.add(full_url)
                if full_url not in visited:
                    links |= crawl_files(full_url, domain, extensions, depth + 1, max_depth, visited, wordlist_file)

        return links

    except Exception as e:
        return set()

# ---------------------
# Example Usage:

if __name__ == "__main__":
    start_url = normalize_url("http://m14r41.in")  # Your base URL
    domain = urlparse(start_url).netloc  # Extract domain from the URL
    extensions = [".js", ".json", ".php", ".txt"]  # Configure your extensions here

    # Start the crawling process and collect links
    links_found = crawl_files(start_url, domain, extensions, wordlist_file="wordlist.txt")

    # Once crawling is finished, print the found links
    print(Fore.GREEN + "[Finished] Found links:")
    for link in links_found:
        print(Fore.GREEN + " -", link)
