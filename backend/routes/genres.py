"""
Genre routes for CRUD operations.
"""
from flask import Blueprint, request
from database import SessionLocal
from models import Genre
from schemas import GenreCreate, GenreUpdate, GenreResponse, GenreWithMovies
from utils.response import (
    success_response,
    error_response,
    not_found_response,
    created_response,
    validation_error_response
)
from pydantic import ValidationError

genres_bp = Blueprint('genres', __name__)


@genres_bp.route('', methods=['GET'])
def get_genres():
    """
    Get all genres.
    
    Query Parameters:
        include_movies (bool): Include movies for each genre
    
    Returns:
        200: List of genres
    """
    db = SessionLocal()
    try:
        include_movies = request.args.get('include_movies', 'false').lower() == 'true'
        
        genres = db.query(Genre).all()
        
        if include_movies:
            genre_list = [GenreWithMovies.model_validate(genre).model_dump() for genre in genres]
        else:
            genre_list = [GenreResponse.model_validate(genre).model_dump() for genre in genres]
        
        return success_response(
            data=genre_list,
            message=f"Retrieved {len(genre_list)} genres"
        )
    
    except Exception as e:
        return error_response(f"Error retrieving genres: {str(e)}", 500)
    
    finally:
        db.close()


@genres_bp.route('/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    """
    Get a specific genre by ID.
    
    Path Parameters:
        genre_id (int): Genre ID
    
    Query Parameters:
        include_movies (bool): Include movies in this genre
    
    Returns:
        200: Genre details
        404: Genre not found
    """
    db = SessionLocal()
    try:
        include_movies = request.args.get('include_movies', 'false').lower() == 'true'
        
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        
        if not genre:
            return not_found_response(f"Genre with ID {genre_id} not found")
        
        if include_movies:
            genre_data = GenreWithMovies.model_validate(genre).model_dump()
        else:
            genre_data = GenreResponse.model_validate(genre).model_dump()
        
        return success_response(data=genre_data)
    
    except Exception as e:
        return error_response(f"Error retrieving genre: {str(e)}", 500)
    
    finally:
        db.close()


@genres_bp.route('', methods=['POST'])
def create_genre():
    """
    Create a new genre.
    
    Request Body:
        GenreCreate schema
    
    Returns:
        201: Created genre
        400: Validation error
    """
    db = SessionLocal()
    try:
        data = request.get_json()
        
        # Validate with Pydantic
        genre_schema = GenreCreate(**data)
        
        # Check if genre with same name already exists
        existing = db.query(Genre).filter(Genre.name == genre_schema.name).first()
        if existing:
            return error_response(f"Genre '{genre_schema.name}' already exists", 400)
        
        # Create new genre
        genre = Genre(**genre_schema.model_dump())
        db.add(genre)
        db.commit()
        db.refresh(genre)
        
        genre_data = GenreResponse.model_validate(genre).model_dump()
        
        return created_response(
            data=genre_data,
            message="Genre created successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error creating genre: {str(e)}", 500)
    
    finally:
        db.close()


@genres_bp.route('/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    """
    Update a genre.
    
    Path Parameters:
        genre_id (int): Genre ID
    
    Request Body:
        GenreUpdate schema
    
    Returns:
        200: Updated genre
        404: Genre not found
        400: Validation error
    """
    db = SessionLocal()
    try:
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        
        if not genre:
            return not_found_response(f"Genre with ID {genre_id} not found")
        
        data = request.get_json()
        genre_schema = GenreUpdate(**data)
        
        # Update only provided fields
        update_data = genre_schema.model_dump(exclude_unset=True)
        
        # Check name uniqueness if updating name
        if 'name' in update_data and update_data['name'] != genre.name:
            existing = db.query(Genre).filter(Genre.name == update_data['name']).first()
            if existing:
                return error_response(f"Genre '{update_data['name']}' already exists", 400)
        
        for key, value in update_data.items():
            setattr(genre, key, value)
        
        db.commit()
        db.refresh(genre)
        
        genre_data = GenreResponse.model_validate(genre).model_dump()
        
        return success_response(
            data=genre_data,
            message="Genre updated successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error updating genre: {str(e)}", 500)
    
    finally:
        db.close()


@genres_bp.route('/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    """
    Delete a genre.
    
    Path Parameters:
        genre_id (int): Genre ID
    
    Returns:
        200: Genre deleted
        404: Genre not found
    """
    db = SessionLocal()
    try:
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        
        if not genre:
            return not_found_response(f"Genre with ID {genre_id} not found")
        
        db.delete(genre)
        db.commit()
        
        return success_response(
            data={"id": genre_id},
            message="Genre deleted successfully"
        )
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error deleting genre: {str(e)}", 500)
    
    finally:
        db.close()