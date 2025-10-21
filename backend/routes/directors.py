"""
Director routes for CRUD operations.
"""
from flask import Blueprint, request
from database import SessionLocal
from models import Director
from schemas import DirectorCreate, DirectorUpdate, DirectorResponse, DirectorWithMovies
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

directors_bp = Blueprint('directors', __name__)
config = get_config()


@directors_bp.route('', methods=['GET'])
def get_directors():
    """
    Get all directors with optional pagination.
    
    Query Parameters:
        page (int): Page number (default: 1)
        page_size (int): Items per page (default: 20)
        include_movies (bool): Include director's movies
    
    Returns:
        200: List of directors
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
        query = db.query(Director)
        total_items = query.count()
        
        directors = query.offset((page - 1) * page_size).limit(page_size).all()
        
        if include_movies:
            director_list = [DirectorWithMovies.model_validate(director).model_dump() for director in directors]
        else:
            director_list = [DirectorResponse.model_validate(director).model_dump() for director in directors]
        
        return paginated_response(
            data=director_list,
            page=page,
            page_size=page_size,
            total_items=total_items
        )
    
    except ValueError:
        return error_response("Invalid pagination parameters", 400)
    
    except Exception as e:
        return error_response(f"Error retrieving directors: {str(e)}", 500)
    
    finally:
        db.close()


@directors_bp.route('/<int:director_id>', methods=['GET'])
def get_director(director_id):
    """
    Get a specific director by ID.
    
    Path Parameters:
        director_id (int): Director ID
    
    Query Parameters:
        include_movies (bool): Include director's movies
    
    Returns:
        200: Director details
        404: Director not found
    """
    db = SessionLocal()
    try:
        include_movies = request.args.get('include_movies', 'false').lower() == 'true'
        
        director = db.query(Director).filter(Director.id == director_id).first()
        
        if not director:
            return not_found_response(f"Director with ID {director_id} not found")
        
        if include_movies:
            director_data = DirectorWithMovies.model_validate(director).model_dump()
        else:
            director_data = DirectorResponse.model_validate(director).model_dump()
        
        return success_response(data=director_data)
    
    except Exception as e:
        return error_response(f"Error retrieving director: {str(e)}", 500)
    
    finally:
        db.close()


@directors_bp.route('', methods=['POST'])
def create_director():
    """
    Create a new director.
    
    Request Body:
        DirectorCreate schema
    
    Returns:
        201: Created director
        400: Validation error
    """
    db = SessionLocal()
    try:
        data = request.get_json()
        director_schema = DirectorCreate(**data)
        
        # Create new director
        director = Director(**director_schema.model_dump())
        db.add(director)
        db.commit()
        db.refresh(director)
        
        director_data = DirectorResponse.model_validate(director).model_dump()
        
        return created_response(
            data=director_data,
            message="Director created successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error creating director: {str(e)}", 500)
    
    finally:
        db.close()


@directors_bp.route('/<int:director_id>', methods=['PUT'])
def update_director(director_id):
    """
    Update a director.
    
    Path Parameters:
        director_id (int): Director ID
    
    Request Body:
        DirectorUpdate schema
    
    Returns:
        200: Updated director
        404: Director not found
        400: Validation error
    """
    db = SessionLocal()
    try:
        director = db.query(Director).filter(Director.id == director_id).first()
        
        if not director:
            return not_found_response(f"Director with ID {director_id} not found")
        
        data = request.get_json()
        director_schema = DirectorUpdate(**data)
        
        # Update only provided fields
        update_data = director_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(director, key, value)
        
        db.commit()
        db.refresh(director)
        
        director_data = DirectorResponse.model_validate(director).model_dump()
        
        return success_response(
            data=director_data,
            message="Director updated successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error updating director: {str(e)}", 500)
    
    finally:
        db.close()


@directors_bp.route('/<int:director_id>', methods=['DELETE'])
def delete_director(director_id):
    """
    Delete a director.
    
    Path Parameters:
        director_id (int): Director ID
    
    Returns:
        200: Director deleted
        404: Director not found
    """
    db = SessionLocal()
    try:
        director = db.query(Director).filter(Director.id == director_id).first()
        
        if not director:
            return not_found_response(f"Director with ID {director_id} not found")
        
        db.delete(director)
        db.commit()
        
        return success_response(
            data={"id": director_id},
            message="Director deleted successfully"
        )
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error deleting director: {str(e)}", 500)
    
    finally:
        db.close()