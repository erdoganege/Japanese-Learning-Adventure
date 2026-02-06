import json
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_entry(entry):
    """Save a JSON entry as day's learning log"""
    file_path = DATA_DIR / f"{entry['date']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)


def load_all_entries():
    """Load all JSON entries from data dir"""
    entries = []
    for file in DATA_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            entries.append(json.load(f))
    return sorted(entries, key=lambda x: x["date"], reverse=True)

def load_all_words():
    """Load all words from data dir"""
    words = []
    for file in DATA_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            entry = json.load(f)
            for w in entry.get("words", []):
                words.append(w)
    return words
