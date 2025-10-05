"""
Movie model for the core movie entity.
"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
from models.associations import movie_actors, movie_genres


class Movie(Base):
    """
    Movie model representing films in the database.
    
    Attributes:
        id: Primary key
        title: Movie title
        description: Movie plot/synopsis
        release_year: Year the movie was released
        duration_minutes: Runtime in minutes
        rating: Movie rating (0-10 scale)
        poster_url: URL to movie poster image
        director_id: Foreign key to director
        director: Relationship to Director
        actors: Relationship to Actors (many-to-many)
        genres: Relationship to Genres (many-to-many)
    """
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    release_year = Column(Integer, nullable=False, index=True)
    duration_minutes = Column(Integer)
    rating = Column(Float, default=0.0)
    poster_url = Column(String(500))
    
    # Foreign Keys
    director_id = Column(
        Integer,
        ForeignKey('directors.id', ondelete='SET NULL'),
        index=True
    )
    
    # Relationships
    director = relationship('Director', back_populates='movies')
    actors = relationship(
        'Actor',
        secondary=movie_actors,
        back_populates='movies',
        lazy='dynamic'
    )
    genres = relationship(
        'Genre',
        secondary=movie_genres,
        back_populates='movies',
        lazy='dynamic'
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint('release_year >= 1888 AND release_year <= 2100', name='valid_year'),
        CheckConstraint('rating >= 0.0 AND rating <= 10.0', name='valid_rating'),
        CheckConstraint('duration_minutes > 0', name='valid_duration'),
    )
    
    def __repr__(self):
        """String representation of Movie."""
        return f"<Movie(id={self.id}, title='{self.title}', year={self.release_year})>"
    
    def to_dict(self, include_relations=False):
        """
        Convert movie to dictionary.
        
        Args:
            include_relations: Whether to include related data (actors, director, genres)
            
        Returns:
            dict: Movie data
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_year': self.release_year,
            'duration_minutes': self.duration_minutes,
            'rating': self.rating,
            'poster_url': self.poster_url
        }
        
        if include_relations:
            # Include director info
            if self.director:
                data['director'] = {
                    'id': self.director.id,
                    'name': self.director.name
                }
            else:
                data['director'] = None
            
            # Include actors
            data['actors'] = [
                {
                    'id': actor.id,
                    'name': actor.name
                }
                for actor in self.actors
            ]
            
            # Include genres
            data['genres'] = [
                {
                    'id': genre.id,
                    'name': genre.name
                }
                for genre in self.genres
            ]
        else:
            # Basic info only
            data['director_id'] = self.director_id
        
        return data
    
    def to_summary_dict(self):
        """
        Convert movie to summary dictionary for list views.
        
        Returns:
            dict: Summarized movie data
        """
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
            'rating': self.rating,
            'poster_url': self.poster_url,
            'director': {
                'id': self.director.id,
                'name': self.director.name
            } if self.director else None,
            'genres': [genre.name for genre in self.genres]
        }