"""
Association tables for many-to-many relationships.
These tables link movies with actors and genres.
"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

# Association table for Movie-Actor relationship (many-to-many)
movie_actors = Table(
    'movie_actors',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id', ondelete='CASCADE'), primary_key=True)
)

# Association table for Movie-Genre relationship (many-to-many)
movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)