"""
Schemas package initialization.
Exports all schema classes for easy importing.
"""
from schemas.base import BaseSchema
from schemas.genre import (
    GenreBase,
    GenreCreate,
    GenreUpdate,
    GenreResponse,
    GenreWithMovies
)
from schemas.director import (
    DirectorBase,
    DirectorCreate,
    DirectorUpdate,
    DirectorResponse,
    DirectorWithMovies
)
from schemas.actor import (
    ActorBase,
    ActorCreate,
    ActorUpdate,
    ActorResponse,
    ActorWithMovies
)
from schemas.movie import (
    MovieBase,
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MovieSummary,
    GenreSummary,
    ActorSummary,
    DirectorSummary
)

__all__ = [
    # Base
    'BaseSchema',
    
    # Genre schemas
    'GenreBase',
    'GenreCreate',
    'GenreUpdate',
    'GenreResponse',
    'GenreWithMovies',
    
    # Director schemas
    'DirectorBase',
    'DirectorCreate',
    'DirectorUpdate',
    'DirectorResponse',
    'DirectorWithMovies',
    
    # Actor schemas
    'ActorBase',
    'ActorCreate',
    'ActorUpdate',
    'ActorResponse',
    'ActorWithMovies',
    
    # Movie schemas
    'MovieBase',
    'MovieCreate',
    'MovieUpdate',
    'MovieResponse',
    'MovieSummary',
    'GenreSummary',
    'ActorSummary',
    'DirectorSummary',
]