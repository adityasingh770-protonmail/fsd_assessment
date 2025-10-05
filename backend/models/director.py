"""
Director model for movie directors.
"""
from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from database import Base


class Director(Base):
    """
    Director model representing film directors.
    
    Attributes:
        id: Primary key
        name: Director's full name
        bio: Biography/description
        birth_date: Date of birth
        nationality: Director's nationality
        movies: Relationship to directed movies
    """
    __tablename__ = 'directors'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    bio = Column(Text)
    birth_date = Column(Date)
    nationality = Column(String(100))
    
    # Relationships
    movies = relationship(
        'Movie',
        back_populates='director',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        """String representation of Director."""
        return f"<Director(id={self.id}, name='{self.name}')>"
    
    def to_dict(self, include_movies=False):
        """
        Convert director to dictionary.
        
        Args:
            include_movies: Whether to include directed movies
            
        Returns:
            dict: Director data
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
        
        return data