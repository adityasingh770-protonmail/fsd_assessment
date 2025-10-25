"""
Director service layer for business logic.
Handles all director-related operations and data manipulation.
"""
from typing import Optional, List, Dict, Tuple
from sqlalchemy.orm import Session
from models import Director
from schemas import DirectorCreate, DirectorUpdate


class DirectorService:
    """Service class for director-related business logic."""

    @staticmethod
    def get_directors_paginated(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        include_movies: bool = False
    ) -> Tuple[List[Director], int]:
        """
        Get paginated list of directors.

        Args:
            db: Database session
            page: Page number (1-indexed)
            page_size: Number of items per page
            include_movies: Whether to include movie relationships

        Returns:
            Tuple of (list of directors, total count)
        """
        query = db.query(Director)
        total_items = query.count()

        directors = query.offset((page - 1) * page_size).limit(page_size).all()

        return directors, total_items

    @staticmethod
    def get_director_by_id(db: Session, director_id: int) -> Optional[Director]:
        """
        Get a single director by ID.

        Args:
            db: Database session
            director_id: Director ID

        Returns:
            Director object or None if not found
        """
        return db.query(Director).filter(Director.id == director_id).first()

    @staticmethod
    def create_director(db: Session, director_data: DirectorCreate) -> Director:
        """
        Create a new director.

        Args:
            db: Database session
            director_data: Validated director creation data

        Returns:
            Created director object
        """
        director = Director(**director_data.model_dump())
        db.add(director)
        db.commit()
        db.refresh(director)

        return director

    @staticmethod
    def update_director(
        db: Session,
        director_id: int,
        director_data: DirectorUpdate
    ) -> Optional[Director]:
        """
        Update an existing director.

        Args:
            db: Database session
            director_id: Director ID to update
            director_data: Validated director update data

        Returns:
            Updated director object or None if not found
        """
        director = db.query(Director).filter(Director.id == director_id).first()

        if not director:
            return None

        # Update only provided fields
        update_dict = director_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(director, key, value)

        db.commit()
        db.refresh(director)

        return director

    @staticmethod
    def delete_director(db: Session, director_id: int) -> bool:
        """
        Delete a director by ID.

        Args:
            db: Database session
            director_id: Director ID to delete

        Returns:
            True if deleted, False if not found
        """
        director = db.query(Director).filter(Director.id == director_id).first()

        if not director:
            return False

        db.delete(director)
        db.commit()

        return True

    @staticmethod
    def serialize_director_summary(director: Director) -> Dict:
        """
        Serialize director to summary format for list views.

        Args:
            director: Director object

        Returns:
            Dictionary with summarized director data
        """
        return {
            'id': director.id,
            'name': director.name,
            'bio': director.bio,
            'birth_date': director.birth_date.isoformat() if director.birth_date else None,
            'nationality': director.nationality
        }

    @staticmethod
    def serialize_director_with_movies(director: Director) -> Dict:
        """
        Serialize director with full movie details.

        Args:
            director: Director object

        Returns:
            Dictionary with director data including filmography
        """
        # Get unique genres from all movies
        genres = set()
        for movie in director.movies:
            for genre in movie.genres:
                genres.add(genre.name)

        return {
            'id': director.id,
            'name': director.name,
            'bio': director.bio,
            'birth_date': director.birth_date.isoformat() if director.birth_date else None,
            'nationality': director.nationality,
            'movies': [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'release_year': movie.release_year,
                    'rating': movie.rating,
                    'poster_url': movie.poster_url,
                    'genres': [genre.name for genre in movie.genres]
                }
                for movie in director.movies
            ],
            'movie_count': len(director.movies),
            'genres': sorted(list(genres))
        }
