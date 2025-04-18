import os
import json

def load_patterns():
    patterns = []
    pattern_categories = {}
    with open("config/patterns.json", "r") as f:
        raw_patterns = json.load(f)
        for category, keys in raw_patterns.items():
            for key in keys:
                patterns.append(key)
                pattern_categories[key.lower()] = category
    return patterns, pattern_categories

def load_extensions():
    with open("config/extensions.json", "r") as f:
        exts = json.load(f).get("file_extensions", [])
        return list(set(ext if ext.startswith('.') else f'.{ext}' for ext in exts))

def load_wordlists():
    guesses = []
    wordlist_dir = "config/wordlist"
    if os.path.isdir(wordlist_dir):
        for file in os.listdir(wordlist_dir):
            with open(os.path.join(wordlist_dir, file), 'r', encoding='utf-8', errors='ignore') as f:
                guesses.extend([line.strip() for line in f if line.strip() and not line.startswith("#")])
    return guesses
