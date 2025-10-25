"""
Genre service layer for business logic.
Handles all genre-related operations and data manipulation.
"""
from typing import Optional, List, Dict, Tuple
from sqlalchemy.orm import Session
from models import Genre
from schemas import GenreCreate, GenreUpdate


class GenreService:
    """Service class for genre-related business logic."""

    @staticmethod
    def get_genres_paginated(
        db: Session,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Genre], int]:
        """
        Get paginated list of genres.

        Args:
            db: Database session
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Tuple of (list of genres, total count)
        """
        query = db.query(Genre)
        total_items = query.count()

        genres = query.offset((page - 1) * page_size).limit(page_size).all()

        return genres, total_items

    @staticmethod
    def get_all_genres(db: Session) -> List[Genre]:
        """
        Get all genres without pagination.

        Args:
            db: Database session

        Returns:
            List of all genres
        """
        return db.query(Genre).all()

    @staticmethod
    def get_genre_by_id(db: Session, genre_id: int) -> Optional[Genre]:
        """
        Get a single genre by ID.

        Args:
            db: Database session
            genre_id: Genre ID

        Returns:
            Genre object or None if not found
        """
        return db.query(Genre).filter(Genre.id == genre_id).first()

    @staticmethod
    def get_genre_by_name(db: Session, name: str) -> Optional[Genre]:
        """
        Get a single genre by name.

        Args:
            db: Database session
            name: Genre name

        Returns:
            Genre object or None if not found
        """
        return db.query(Genre).filter(Genre.name == name).first()

    @staticmethod
    def create_genre(db: Session, genre_data: GenreCreate) -> Genre:
        """
        Create a new genre.

        Args:
            db: Database session
            genre_data: Validated genre creation data

        Returns:
            Created genre object

        Raises:
            ValueError: If genre with same name already exists
        """
        # Check if genre with same name exists
        existing = GenreService.get_genre_by_name(db, genre_data.name)
        if existing:
            raise ValueError(f"Genre with name '{genre_data.name}' already exists")

        genre = Genre(**genre_data.model_dump())
        db.add(genre)
        db.commit()
        db.refresh(genre)

        return genre

    @staticmethod
    def update_genre(
        db: Session,
        genre_id: int,
        genre_data: GenreUpdate
    ) -> Optional[Genre]:
        """
        Update an existing genre.

        Args:
            db: Database session
            genre_id: Genre ID to update
            genre_data: Validated genre update data

        Returns:
            Updated genre object or None if not found

        Raises:
            ValueError: If updated name conflicts with existing genre
        """
        genre = db.query(Genre).filter(Genre.id == genre_id).first()

        if not genre:
            return None

        # Check if new name conflicts with existing genre
        update_dict = genre_data.model_dump(exclude_unset=True)
        if 'name' in update_dict:
            existing = GenreService.get_genre_by_name(db, update_dict['name'])
            if existing and existing.id != genre_id:
                raise ValueError(f"Genre with name '{update_dict['name']}' already exists")

        # Update fields
        for key, value in update_dict.items():
            setattr(genre, key, value)

        db.commit()
        db.refresh(genre)

        return genre

    @staticmethod
    def delete_genre(db: Session, genre_id: int) -> bool:
        """
        Delete a genre by ID.

        Args:
            db: Database session
            genre_id: Genre ID to delete

        Returns:
            True if deleted, False if not found
        """
        genre = db.query(Genre).filter(Genre.id == genre_id).first()

        if not genre:
            return False

        db.delete(genre)
        db.commit()

        return True

    @staticmethod
    def serialize_genre(genre: Genre, include_movie_count: bool = False) -> Dict:
        """
        Serialize genre to dictionary format.

        Args:
            genre: Genre object
            include_movie_count: Whether to include count of movies in this genre

        Returns:
            Dictionary with genre data
        """
        data = {
            'id': genre.id,
            'name': genre.name,
            'description': genre.description
        }

        if include_movie_count:
            data['movie_count'] = genre.movies.count()

        return data
