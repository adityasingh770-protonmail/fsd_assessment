"""
Movie routes for CRUD operations with filtering.
Routes are responsible for HTTP handling only.
Business logic is delegated to MovieService.
Database sessions are managed by the service layer.
"""
from flask import Blueprint, request
from schemas import MovieCreate, MovieUpdate
from services import MovieService
from utils.response import (
    success_response,
    error_response,
    not_found_response,
    created_response,
    validation_error_response,
    paginated_response
)
from utils.validators import validate_page_number, validate_page_size, sanitize_search_query
from pydantic import ValidationError
from config import get_config

movies_bp = Blueprint('movies', __name__)
config = get_config()


@movies_bp.route('', methods=['GET'])
def get_movies():
    """
    Get all movies with optional filtering and pagination.

    Query Parameters:
        page (int): Page number (default: 1)
        page_size (int): Items per page (default: 20)
        genre (str): Filter by genre name
        director (str): Filter by director name
        actor (str): Filter by actor name
        year (int): Filter by release year
        search (str): Search in title and description
        min_rating (float): Minimum rating filter
        max_rating (float): Maximum rating filter

    Returns:
        200: List of movies
    """
    try:
        # Extract and validate pagination parameters
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', config.DEFAULT_PAGE_SIZE))

        if not validate_page_number(page):
            return error_response("Invalid page number", 400)

        if not validate_page_size(page_size, config.MAX_PAGE_SIZE):
            return error_response(f"Page size must be between 1 and {config.MAX_PAGE_SIZE}", 400)

        # Extract filter parameters
        genre = request.args.get('genre')
        director = request.args.get('director')
        actor = request.args.get('actor')
        year = request.args.get('year')
        search = request.args.get('search')
        min_rating = request.args.get('min_rating')
        max_rating = request.args.get('max_rating')

        # Validate and convert numeric parameters
        if year:
            try:
                year = int(year)
            except ValueError:
                return error_response("Invalid year parameter", 400)

        if min_rating:
            try:
                min_rating = float(min_rating)
            except ValueError:
                return error_response("Invalid min_rating parameter", 400)

        if max_rating:
            try:
                max_rating = float(max_rating)
            except ValueError:
                return error_response("Invalid max_rating parameter", 400)

        # Sanitize search query
        if search:
            search = sanitize_search_query(search)

        # Delegate to service layer (returns serialized dicts)
        movie_list, total_items = MovieService.get_movies_with_filters(
            page=page,
            page_size=page_size,
            genre=genre,
            director=director,
            actor=actor,
            year=year,
            search=search,
            min_rating=min_rating,
            max_rating=max_rating
        )

        return paginated_response(
            data=movie_list,
            page=page,
            page_size=page_size,
            total_items=total_items
        )

    except ValueError as e:
        return error_response(f"Invalid parameter: {str(e)}", 400)

    except Exception as e:
        return error_response(f"Error retrieving movies: {str(e)}", 500)


@movies_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Get a specific movie by ID with full details.

    Path Parameters:
        movie_id (int): Movie ID

    Returns:
        200: Movie details with cast, director, and genres
        404: Movie not found
    """
    try:
        # Delegate to service layer (returns serialized dict or None)
        movie_data = MovieService.get_movie_by_id(movie_id)

        if not movie_data:
            return not_found_response(f"Movie with ID {movie_id} not found")

        return success_response(data=movie_data)

    except Exception as e:
        return error_response(f"Error retrieving movie: {str(e)}", 500)


@movies_bp.route('', methods=['POST'])
def create_movie():
    """
    Create a new movie.

    Request Body:
        MovieCreate schema (includes director_id, actor_ids, genre_ids)

    Returns:
        201: Created movie
        400: Validation error
        404: Related entity not found
    """
    try:
        # Validate request data
        data = request.get_json()
        movie_schema = MovieCreate(**data)

        # Delegate to service layer (returns serialized dict)
        movie_response = MovieService.create_movie(movie_schema)

        return created_response(
            data=movie_response,
            message="Movie created successfully"
        )

    except ValidationError as e:
        return validation_error_response(e.errors())

    except ValueError as e:
        # Service layer raises ValueError for business logic errors
        return not_found_response(str(e))

    except Exception as e:
        return error_response(f"Error creating movie: {str(e)}", 500)


@movies_bp.route('/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """
    Update a movie.

    Path Parameters:
        movie_id (int): Movie ID

    Request Body:
        MovieUpdate schema

    Returns:
        200: Updated movie
        404: Movie not found
        400: Validation error
    """
    try:
        # Validate request data
        data = request.get_json()
        movie_schema = MovieUpdate(**data)

        # Delegate to service layer (returns serialized dict or None)
        movie_response = MovieService.update_movie(movie_id, movie_schema)

        if not movie_response:
            return not_found_response(f"Movie with ID {movie_id} not found")

        return success_response(
            data=movie_response,
            message="Movie updated successfully"
        )

    except ValidationError as e:
        return validation_error_response(e.errors())

    except ValueError as e:
        # Service layer raises ValueError for business logic errors
        return not_found_response(str(e))

    except Exception as e:
        return error_response(f"Error updating movie: {str(e)}", 500)


@movies_bp.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """
    Delete a movie.

    Path Parameters:
        movie_id (int): Movie ID

    Returns:
        200: Movie deleted
        404: Movie not found
    """
    try:
        # Delegate to service layer (returns boolean)
        deleted = MovieService.delete_movie(movie_id)

        if not deleted:
            return not_found_response(f"Movie with ID {movie_id} not found")

        return success_response(
            data={"id": movie_id},
            message="Movie deleted successfully"
        )

    except Exception as e:
        return error_response(f"Error deleting movie: {str(e)}", 500)
