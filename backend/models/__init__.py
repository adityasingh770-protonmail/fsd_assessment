"""
Models package initialization.
Imports all models to ensure they are registered with SQLAlchemy.
"""
from models.movie import Movie
from models.actor import Actor
from models.director import Director
from models.genre import Genre
from models.associations import movie_actors, movie_genres

__all__ = [
    'Movie',
    'Actor',
    'Director',
    'Genre',
    'movie_actors',
    'movie_genres'
]