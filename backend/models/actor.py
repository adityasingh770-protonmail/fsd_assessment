"""
Actor model for movie cast members.
"""
from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from database import Base
from models.associations import movie_actors


class Actor(Base):
    """
    Actor model representing film actors/actresses.
    
    Attributes:
        id: Primary key
        name: Actor's full name
        bio: Biography/description
        birth_date: Date of birth
        nationality: Actor's nationality
        movies: Relationship to movies they've appeared in
    """
    __tablename__ = 'actors'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    bio = Column(Text)
    birth_date = Column(Date)
    nationality = Column(String(100))
    
    # Relationships
    movies = relationship(
        'Movie',
        secondary=movie_actors,
        back_populates='actors',
        lazy='dynamic'
    )
    
    def __repr__(self):
        """String representation of Actor."""
        return f"<Actor(id={self.id}, name='{self.name}')>"
    
    def to_dict(self, include_movies=False):
        """
        Convert actor to dictionary.
        
        Args:
            include_movies: Whether to include movies they've acted in
            
        Returns:
            dict: Actor data
        """
        data = {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'nationality': self.nationality
        }
        
        if include_movies:
            data['movies'] = [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'release_year': movie.release_year,
                    'rating': movie.rating
                }
                for movie in self.movies
            ]
            data['movie_count'] = self.movies.count()
            
            # Get unique genres this actor has worked in
            genres = set()
            for movie in self.movies:
                for genre in movie.genres:
                    genres.add(genre.name)
            data['genres'] = sorted(list(genres))
        
        return data