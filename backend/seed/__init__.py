"""
Seed package for loading sample data from JSON files.
"""
import json
import os
from typing import List, Dict


def load_json_file(filename: str) -> List[Dict]:
    """Load data from a JSON file in the seed directory."""
    seed_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(seed_dir, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filename} in seed directory")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filename}: {e}")
        return []


def load_genres() -> List[Dict]:
    """Load genres from genres.json."""
    return load_json_file('genres.json')


def load_directors() -> List[Dict]:
    """Load directors from directors.json."""
    return load_json_file('directors.json')


def load_actors() -> List[Dict]:
    """Load actors from actors.json."""
    return load_json_file('actors.json')


def load_movies() -> List[Dict]:
    """Load movies from movies.json."""
    return load_json_file('movies.json')


__all__ = [
    'load_genres',
    'load_directors',
    'load_actors',
    'load_movies',
]