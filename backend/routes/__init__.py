"""
Routes package initialization.
Exports all blueprint instances for registration in the main app.
"""
from routes.movies import movies_bp
from routes.actors import actors_bp
from routes.directors import directors_bp
from routes.genres import genres_bp

__all__ = [
    'movies_bp',
    'actors_bp',
    'directors_bp',
    'genres_bp',
]