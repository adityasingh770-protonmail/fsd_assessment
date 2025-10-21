"""
Actor routes for CRUD operations.
"""
from flask import Blueprint, request
from database import SessionLocal
from models import Actor
from schemas import ActorCreate, ActorUpdate, ActorResponse, ActorWithMovies
from utils.response import (
    success_response,
    error_response,
    not_found_response,
    created_response,
    validation_error_response,
    paginated_response
)
from utils.validators import validate_page_number, validate_page_size
from pydantic import ValidationError
from config import get_config

actors_bp = Blueprint('actors', __name__)
config = get_config()


@actors_bp.route('', methods=['GET'])
def get_actors():
    """
    Get all actors with optional pagination.
    
    Query Parameters:
        page (int): Page number (default: 1)
        page_size (int): Items per page (default: 20)
        include_movies (bool): Include actor's movies
    
    Returns:
        200: List of actors
    """
    db = SessionLocal()
    try:
        # Pagination parameters
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', config.DEFAULT_PAGE_SIZE))
        include_movies = request.args.get('include_movies', 'false').lower() == 'true'
        
        # Validate pagination
        if not validate_page_number(page):
            return error_response("Invalid page number", 400)
        
        if not validate_page_size(page_size, config.MAX_PAGE_SIZE):
            return error_response(f"Page size must be between 1 and {config.MAX_PAGE_SIZE}", 400)
        
        # Query with pagination
        query = db.query(Actor)
        total_items = query.count()
        
        actors = query.offset((page - 1) * page_size).limit(page_size).all()
        
        actor_list = []
        for actor in actors:
            actor_dict = {
                'id': actor.id,
                'name': actor.name,
                'bio': actor.bio,
                'birth_date': actor.birth_date.isoformat() if actor.birth_date else None,
                'nationality': actor.nationality
            }
            
            if include_movies:
                actor_dict['movies'] = [
                    {
                        'id': movie.id,
                        'title': movie.title,
                        'release_year': movie.release_year,
                        'rating': movie.rating
                    }
                    for movie in actor.movies
                ]
                actor_dict['movie_count'] = actor.movies.count()
                genres = set()
                for movie in actor.movies:
                    for genre in movie.genres:
                        genres.add(genre.name)
                actor_dict['genres'] = sorted(list(genres))
            
            actor_list.append(actor_dict)
        
        return paginated_response(
            data=actor_list,
            page=page,
            page_size=page_size,
            total_items=total_items
        )
    
    except ValueError:
        return error_response("Invalid pagination parameters", 400)
    
    except Exception as e:
        return error_response(f"Error retrieving actors: {str(e)}", 500)
    
    finally:
        db.close()


@actors_bp.route('/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    """
    Get a specific actor by ID.
    
    Path Parameters:
        actor_id (int): Actor ID
    
    Query Parameters:
        include_movies (bool): Include actor's movies
    
    Returns:
        200: Actor details
        404: Actor not found
    """
    db = SessionLocal()
    try:
        include_movies = request.args.get('include_movies', 'false').lower() == 'true'
        
        actor = db.query(Actor).filter(Actor.id == actor_id).first()
        
        if not actor:
            return not_found_response(f"Actor with ID {actor_id} not found")
        
        actor_data = {
            'id': actor.id,
            'name': actor.name,
            'bio': actor.bio,
            'birth_date': actor.birth_date.isoformat() if actor.birth_date else None,
            'nationality': actor.nationality
        }
        
        if include_movies:
            actor_data['movies'] = [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'release_year': movie.release_year,
                    'rating': movie.rating
                }
                for movie in actor.movies
            ]
            actor_data['movie_count'] = actor.movies.count()
            genres = set()
            for movie in actor.movies:
                for genre in movie.genres:
                    genres.add(genre.name)
            actor_data['genres'] = sorted(list(genres))
        
        return success_response(data=actor_data)
    
    except Exception as e:
        return error_response(f"Error retrieving actor: {str(e)}", 500)
    
    finally:
        db.close()


@actors_bp.route('', methods=['POST'])
def create_actor():
    """
    Create a new actor.
    
    Request Body:
        ActorCreate schema
    
    Returns:
        201: Created actor
        400: Validation error
    """
    db = SessionLocal()
    try:
        data = request.get_json()
        actor_schema = ActorCreate(**data)
        
        # Create new actor
        actor = Actor(**actor_schema.model_dump())
        db.add(actor)
        db.commit()
        db.refresh(actor)
        
        actor_data = {
            'id': actor.id,
            'name': actor.name,
            'bio': actor.bio,
            'birth_date': actor.birth_date.isoformat() if actor.birth_date else None,
            'nationality': actor.nationality
        }
        
        return created_response(
            data=actor_data,
            message="Actor created successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error creating actor: {str(e)}", 500)
    
    finally:
        db.close()


@actors_bp.route('/<int:actor_id>', methods=['PUT'])
def update_actor(actor_id):
    """
    Update an actor.
    
    Path Parameters:
        actor_id (int): Actor ID
    
    Request Body:
        ActorUpdate schema
    
    Returns:
        200: Updated actor
        404: Actor not found
        400: Validation error
    """
    db = SessionLocal()
    try:
        actor = db.query(Actor).filter(Actor.id == actor_id).first()
        
        if not actor:
            return not_found_response(f"Actor with ID {actor_id} not found")
        
        data = request.get_json()
        actor_schema = ActorUpdate(**data)
        
        # Update only provided fields
        update_data = actor_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(actor, key, value)
        
        db.commit()
        db.refresh(actor)
        
        actor_data = {
            'id': actor.id,
            'name': actor.name,
            'bio': actor.bio,
            'birth_date': actor.birth_date.isoformat() if actor.birth_date else None,
            'nationality': actor.nationality
        }
        
        return success_response(
            data=actor_data,
            message="Actor updated successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error updating actor: {str(e)}", 500)
    
    finally:
        db.close()


@actors_bp.route('/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    """
    Delete an actor.
    
    Path Parameters:
        actor_id (int): Actor ID
    
    Returns:
        200: Actor deleted
        404: Actor not found
    """
    db = SessionLocal()
    try:
        actor = db.query(Actor).filter(Actor.id == actor_id).first()
        
        if not actor:
            return not_found_response(f"Actor with ID {actor_id} not found")
        
        db.delete(actor)
        db.commit()
        
        return success_response(
            data={"id": actor_id},
            message="Actor deleted successfully"
        )
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error deleting actor: {str(e)}", 500)
    
    finally:
        db.close()