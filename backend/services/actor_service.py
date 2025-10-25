"""
Actor service layer for business logic.
Handles all actor-related operations and data manipulation.
"""
from typing import Optional, List, Dict, Tuple
from sqlalchemy.orm import Session
from models import Actor
from schemas import ActorCreate, ActorUpdate


class ActorService:
    """Service class for actor-related business logic."""

    @staticmethod
    def get_actors_paginated(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        include_movies: bool = False
    ) -> Tuple[List[Actor], int]:
        """
        Get paginated list of actors.

        Args:
            db: Database session
            page: Page number (1-indexed)
            page_size: Number of items per page
            include_movies: Whether to include movie relationships

        Returns:
            Tuple of (list of actors, total count)
        """
        query = db.query(Actor)
        total_items = query.count()

        actors = query.offset((page - 1) * page_size).limit(page_size).all()

        return actors, total_items

    @staticmethod
    def get_actor_by_id(db: Session, actor_id: int) -> Optional[Actor]:
        """
        Get a single actor by ID.

        Args:
            db: Database session
            actor_id: Actor ID

        Returns:
            Actor object or None if not found
        """
        return db.query(Actor).filter(Actor.id == actor_id).first()

    @staticmethod
    def create_actor(db: Session, actor_data: ActorCreate) -> Actor:
        """
        Create a new actor.

        Args:
            db: Database session
            actor_data: Validated actor creation data

        Returns:
            Created actor object
        """
        actor = Actor(**actor_data.model_dump())
        db.add(actor)
        db.commit()
        db.refresh(actor)

        return actor

    @staticmethod
    def update_actor(
        db: Session,
        actor_id: int,
        actor_data: ActorUpdate
    ) -> Optional[Actor]:
        """
        Update an existing actor.

        Args:
            db: Database session
            actor_id: Actor ID to update
            actor_data: Validated actor update data

        Returns:
            Updated actor object or None if not found
        """
        actor = db.query(Actor).filter(Actor.id == actor_id).first()

        if not actor:
            return None

        # Update only provided fields
        update_dict = actor_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(actor, key, value)

        db.commit()
        db.refresh(actor)

        return actor

    @staticmethod
    def delete_actor(db: Session, actor_id: int) -> bool:
        """
        Delete an actor by ID.

        Args:
            db: Database session
            actor_id: Actor ID to delete

        Returns:
            True if deleted, False if not found
        """
        actor = db.query(Actor).filter(Actor.id == actor_id).first()

        if not actor:
            return False

        db.delete(actor)
        db.commit()

        return True

    @staticmethod
    def serialize_actor_summary(actor: Actor) -> Dict:
        """
        Serialize actor to summary format for list views.

        Args:
            actor: Actor object

        Returns:
            Dictionary with summarized actor data
        """
        return {
            'id': actor.id,
            'name': actor.name,
            'bio': actor.bio,
            'birth_date': actor.birth_date.isoformat() if actor.birth_date else None,
            'nationality': actor.nationality
        }

    @staticmethod
    def serialize_actor_with_movies(actor: Actor) -> Dict:
        """
        Serialize actor with full movie details.

        Args:
            actor: Actor object

        Returns:
            Dictionary with actor data including filmography
        """
        # Get unique genres from all movies
        genres = set()
        for movie in actor.movies:
            for genre in movie.genres:
                genres.add(genre.name)

        return {
            'id': actor.id,
            'name': actor.name,
            'bio': actor.bio,
            'birth_date': actor.birth_date.isoformat() if actor.birth_date else None,
            'nationality': actor.nationality,
            'movies': [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'release_year': movie.release_year,
                    'rating': movie.rating,
                    'poster_url': movie.poster_url,
                    'genres': [genre.name for genre in movie.genres]
                }
                for movie in actor.movies
            ],
            'movie_count': actor.movies.count(),
            'genres': sorted(list(genres))
        }
