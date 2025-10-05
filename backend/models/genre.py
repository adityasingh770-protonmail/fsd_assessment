"""
Genre model for movie genres/categories.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.associations import movie_genres


class Genre(Base):
    """
    Genre model representing movie categories.
    
    Attributes:
        id: Primary key
        name: Genre name (e.g., "Action", "Comedy", "Drama")
        description: Optional genre description
        movies: Relationship to movies in this genre
    """
    __tablename__ = 'genres'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(500))
    
    # Relationships
    movies = relationship(
        'Movie',
        secondary=movie_genres,
        back_populates='genres',
        lazy='dynamic'
    )
    
    def __repr__(self):
        """String representation of Genre."""
        return f"<Genre(id={self.id}, name='{self.name}')>"
    
    def to_dict(self, include_movies=False):
        """
        Convert genre to dictionary.
        
        Args:
            include_movies: Whether to include associated movies
            
        Returns:
            dict: Genre data
        """
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        
        if include_movies:
            data['movies'] = [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'release_year': movie.release_year
                }
                for movie in self.movies
            ]
        
        return data