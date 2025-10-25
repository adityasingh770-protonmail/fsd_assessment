"""
Actor routes for CRUD operations.
Routes are responsible for HTTP handling only.
Business logic is delegated to ActorService.
"""
from flask import Blueprint, request
from database import SessionLocal
from schemas import ActorCreate, ActorUpdate
from services import ActorService
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

        # Delegate to service layer
        actors, total_items = ActorService.get_actors_paginated(
            db=db,
            page=page,
            page_size=page_size,
            include_movies=include_movies
        )

        # Serialize actors
        if include_movies:
            actor_list = [ActorService.serialize_actor_with_movies(actor) for actor in actors]
        else:
            actor_list = [ActorService.serialize_actor_summary(actor) for actor in actors]

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

        # Delegate to service layer
        actor = ActorService.get_actor_by_id(db, actor_id)

        if not actor:
            return not_found_response(f"Actor with ID {actor_id} not found")

        # Serialize actor
        if include_movies:
            actor_data = ActorService.serialize_actor_with_movies(actor)
        else:
            actor_data = ActorService.serialize_actor_summary(actor)

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
        # Validate request data
        data = request.get_json()
        actor_schema = ActorCreate(**data)

        # Delegate to service layer
        actor = ActorService.create_actor(db, actor_schema)

        # Serialize response
        actor_data = ActorService.serialize_actor_summary(actor)

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
        # Validate request data
        data = request.get_json()
        actor_schema = ActorUpdate(**data)

        # Delegate to service layer
        actor = ActorService.update_actor(db, actor_id, actor_schema)

        if not actor:
            return not_found_response(f"Actor with ID {actor_id} not found")

        # Serialize response
        actor_data = ActorService.serialize_actor_summary(actor)

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
        # Delegate to service layer
        deleted = ActorService.delete_actor(db, actor_id)

        if not deleted:
            return not_found_response(f"Actor with ID {actor_id} not found")

        return success_response(
            data={"id": actor_id},
            message="Actor deleted successfully"
        )

    except Exception as e:
        db.rollback()
        return error_response(f"Error deleting actor: {str(e)}", 500)

    finally:
        db.close()
