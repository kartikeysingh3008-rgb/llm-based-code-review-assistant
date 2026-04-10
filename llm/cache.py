import json
import hashlib
import os

CACHE_FILE = "llm_cache.json"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def generate_key(code, analysis):
    raw = code + str(analysis)
    return hashlib.md5(raw.encode()).hexdigest()