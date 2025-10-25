"""
Movie service layer for business logic.
Handles all movie-related operations and data manipulation.
Database sessions are managed by the service layer.
"""
from typing import Optional, List, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Movie, Actor, Director, Genre
from schemas import MovieCreate, MovieUpdate
from services.base_service import BaseService


class MovieService(BaseService):
    """Service class for movie-related business logic."""

    @staticmethod
    def get_movies_with_filters(
        page: int = 1,
        page_size: int = 20,
        genre: Optional[str] = None,
        director: Optional[str] = None,
        actor: Optional[str] = None,
        year: Optional[int] = None,
        search: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        db: Optional[Session] = None
    ) -> Tuple[List[Dict], int]:
        """
        Get movies with optional filters and pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            genre: Filter by genre name (partial match)
            director: Filter by director name (partial match)
            actor: Filter by actor name (partial match)
            year: Filter by exact release year
            search: Search in title and description
            min_rating: Minimum rating filter
            max_rating: Maximum rating filter
            db: Optional database session (if None, creates one)

        Returns:
            Tuple of (list of movie dicts, total count)
        """
        session, should_close = MovieService._get_session(db)

        try:
            # Base query
            query = session.query(Movie)

            # Apply filters
            if genre:
                query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre}%"))

            if director:
                query = query.join(Movie.director).filter(Director.name.ilike(f"%{director}%"))

            if actor:
                query = query.join(Movie.actors).filter(Actor.name.ilike(f"%{actor}%"))

            if year:
                query = query.filter(Movie.release_year == year)

            if min_rating is not None:
                query = query.filter(Movie.rating >= min_rating)

            if max_rating is not None:
                query = query.filter(Movie.rating <= max_rating)

            if search:
                query = query.filter(
                    or_(
                        Movie.title.ilike(f"%{search}%"),
                        Movie.description.ilike(f"%{search}%")
                    )
                )

            # Get total count (before pagination)
            total_items = query.distinct().count()

            # Apply pagination
            movies = query.distinct().offset((page - 1) * page_size).limit(page_size).all()

            # Serialize BEFORE closing session (important!)
            movie_dicts = [MovieService.serialize_movie_summary(movie) for movie in movies]

            return movie_dicts, total_items

        finally:
            if should_close:
                session.close()

    @staticmethod
    def get_movie_by_id(movie_id: int, db: Optional[Session] = None) -> Optional[Dict]:
        """
        Get a single movie by ID.

        Args:
            movie_id: Movie ID
            db: Optional database session (if None, creates one)

        Returns:
            Movie dictionary or None if not found
        """
        session, should_close = MovieService._get_session(db)

        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()

            if not movie:
                return None

            # Serialize BEFORE closing session
            return MovieService.serialize_movie_detail(movie)

        finally:
            if should_close:
                session.close()

    @staticmethod
    def create_movie(movie_data: MovieCreate, db: Optional[Session] = None) -> Dict:
        """
        Create a new movie with relationships.

        Args:
            movie_data: Validated movie creation data
            db: Optional database session (if None, creates one)

        Returns:
            Created movie dictionary

        Raises:
            ValueError: If referenced entities (director, actors, genres) don't exist
        """
        session, should_close = MovieService._get_session(db)

        try:
            # Extract relationship IDs
            movie_dict = movie_data.model_dump(exclude={'actor_ids', 'genre_ids'})
            actor_ids = movie_data.actor_ids
            genre_ids = movie_data.genre_ids

            # Validate director exists (if provided)
            if movie_dict.get('director_id'):
                director = session.query(Director).filter(
                    Director.id == movie_dict['director_id']
                ).first()
                if not director:
                    raise ValueError(f"Director with ID {movie_dict['director_id']} not found")

            # Create movie instance
            movie = Movie(**movie_dict)

            # Add actors
            if actor_ids:
                actors = session.query(Actor).filter(Actor.id.in_(actor_ids)).all()
                if len(actors) != len(actor_ids):
                    raise ValueError("One or more actor IDs not found")
                movie.actors.extend(actors)

            # Add genres
            if genre_ids:
                genres = session.query(Genre).filter(Genre.id.in_(genre_ids)).all()
                if len(genres) != len(genre_ids):
                    raise ValueError("One or more genre IDs not found")
                movie.genres.extend(genres)

            # Save to database
            session.add(movie)

            if should_close:
                session.commit()
                session.refresh(movie)

            # Serialize BEFORE closing session
            movie_response = MovieService.serialize_movie_detail(movie)

            return movie_response

        except Exception:
            if should_close:
                session.rollback()
            raise
        finally:
            if should_close:
                session.close()

    @staticmethod
    def update_movie(
        movie_id: int,
        movie_data: MovieUpdate,
        db: Optional[Session] = None
    ) -> Optional[Dict]:
        """
        Update an existing movie.

        Args:
            movie_id: Movie ID to update
            movie_data: Validated movie update data
            db: Optional database session (if None, creates one)

        Returns:
            Updated movie dictionary or None if not found

        Raises:
            ValueError: If referenced entities don't exist
        """
        session, should_close = MovieService._get_session(db)

        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()

            if not movie:
                return None

            # Extract relationship IDs
            update_dict = movie_data.model_dump(
                exclude_unset=True,
                exclude={'actor_ids', 'genre_ids'}
            )

            # Validate director if updating
            if 'director_id' in update_dict and update_dict['director_id']:
                director = session.query(Director).filter(
                    Director.id == update_dict['director_id']
                ).first()
                if not director:
                    raise ValueError(f"Director with ID {update_dict['director_id']} not found")

            # Update basic fields
            for key, value in update_dict.items():
                setattr(movie, key, value)

            # Update actors if provided
            if movie_data.actor_ids is not None:
                actors = session.query(Actor).filter(Actor.id.in_(movie_data.actor_ids)).all()
                if len(actors) != len(movie_data.actor_ids):
                    raise ValueError("One or more actor IDs not found")
                movie.actors.clear()
                movie.actors.extend(actors)

            # Update genres if provided
            if movie_data.genre_ids is not None:
                genres = session.query(Genre).filter(Genre.id.in_(movie_data.genre_ids)).all()
                if len(genres) != len(movie_data.genre_ids):
                    raise ValueError("One or more genre IDs not found")
                movie.genres.clear()
                movie.genres.extend(genres)

            if should_close:
                session.commit()
                session.refresh(movie)

            # Serialize BEFORE closing session
            movie_response = MovieService.serialize_movie_detail(movie)

            return movie_response

        except Exception:
            if should_close:
                session.rollback()
            raise
        finally:
            if should_close:
                session.close()

    @staticmethod
    def delete_movie(movie_id: int, db: Optional[Session] = None) -> bool:
        """
        Delete a movie by ID.

        Args:
            movie_id: Movie ID to delete
            db: Optional database session (if None, creates one)

        Returns:
            True if deleted, False if not found
        """
        session, should_close = MovieService._get_session(db)

        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()

            if not movie:
                return False

            session.delete(movie)

            if should_close:
                session.commit()

            return True

        except Exception:
            if should_close:
                session.rollback()
            raise
        finally:
            if should_close:
                session.close()

    @staticmethod
    def serialize_movie_summary(movie: Movie) -> Dict:
        """
        Serialize movie to summary format for list views.
        MUST be called while session is still open.

        Args:
            movie: Movie object

        Returns:
            Dictionary with summarized movie data
        """
        return {
            'id': movie.id,
            'title': movie.title,
            'release_year': movie.release_year,
            'rating': movie.rating,
            'poster_url': movie.poster_url,
            'director': {
                'id': movie.director.id,
                'name': movie.director.name
            } if movie.director else None,
            'genres': [genre.name for genre in movie.genres]
        }

    @staticmethod
    def serialize_movie_detail(movie: Movie) -> Dict:
        """
        Serialize movie to detailed format.
        MUST be called while session is still open.

        Args:
            movie: Movie object

        Returns:
            Dictionary with full movie data including relationships
        """
        return {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'release_year': movie.release_year,
            'duration_minutes': movie.duration_minutes,
            'rating': movie.rating,
            'poster_url': movie.poster_url,
            'director': {
                'id': movie.director.id,
                'name': movie.director.name
            } if movie.director else None,
            'actors': [
                {'id': actor.id, 'name': actor.name}
                for actor in movie.actors
            ],
            'genres': [
                {'id': genre.id, 'name': genre.name}
                for genre in movie.genres
            ]
        }
