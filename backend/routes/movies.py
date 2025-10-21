"""
Movie routes for CRUD operations with filtering.
"""
from flask import Blueprint, request
from sqlalchemy import or_
from database import SessionLocal
from models import Movie, Actor, Director, Genre
from schemas import MovieCreate, MovieUpdate, MovieResponse, MovieSummary
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
    db = SessionLocal()
    try:
        # Pagination parameters
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', config.DEFAULT_PAGE_SIZE))
        
        # Validate pagination
        if not validate_page_number(page):
            return error_response("Invalid page number", 400)
        
        if not validate_page_size(page_size, config.MAX_PAGE_SIZE):
            return error_response(f"Page size must be between 1 and {config.MAX_PAGE_SIZE}", 400)
        
        # Base query
        query = db.query(Movie)
        
        # Filter by genre
        genre_name = request.args.get('genre')
        if genre_name:
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre_name}%"))
        
        # Filter by director
        director_name = request.args.get('director')
        if director_name:
            query = query.join(Movie.director).filter(Director.name.ilike(f"%{director_name}%"))
        
        # Filter by actor
        actor_name = request.args.get('actor')
        if actor_name:
            query = query.join(Movie.actors).filter(Actor.name.ilike(f"%{actor_name}%"))
        
        # Filter by year
        year = request.args.get('year')
        if year:
            try:
                query = query.filter(Movie.release_year == int(year))
            except ValueError:
                return error_response("Invalid year parameter", 400)
        
        # Filter by rating range
        min_rating = request.args.get('min_rating')
        if min_rating:
            try:
                query = query.filter(Movie.rating >= float(min_rating))
            except ValueError:
                return error_response("Invalid min_rating parameter", 400)
        
        max_rating = request.args.get('max_rating')
        if max_rating:
            try:
                query = query.filter(Movie.rating <= float(max_rating))
            except ValueError:
                return error_response("Invalid max_rating parameter", 400)
        
        # Search in title and description
        search = request.args.get('search')
        if search:
            search_term = sanitize_search_query(search)
            if search_term:
                query = query.filter(
                    or_(
                        Movie.title.ilike(f"%{search_term}%"),
                        Movie.description.ilike(f"%{search_term}%")
                    )
                )
        
        # Get total count before pagination
        total_items = query.distinct().count()
        
        # Apply pagination
        movies = query.distinct().offset((page - 1) * page_size).limit(page_size).all()
        
        # Convert to summary format for list view
        movie_list = []
        for movie in movies:
            movie_dict = {
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
            movie_list.append(movie_dict)
        
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
    
    finally:
        db.close()


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
    db = SessionLocal()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        
        if not movie:
            return not_found_response(f"Movie with ID {movie_id} not found")
        
        movie_data = {
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
        
        return success_response(data=movie_data)
    
    except Exception as e:
        return error_response(f"Error retrieving movie: {str(e)}", 500)
    
    finally:
        db.close()


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
    db = SessionLocal()
    try:
        data = request.get_json()
        movie_schema = MovieCreate(**data)
        
        # Extract relationship IDs
        movie_data = movie_schema.model_dump(exclude={'actor_ids', 'genre_ids'})
        actor_ids = movie_schema.actor_ids
        genre_ids = movie_schema.genre_ids
        
        # Validate director exists
        if movie_data.get('director_id'):
            director = db.query(Director).filter(Director.id == movie_data['director_id']).first()
            if not director:
                return not_found_response(f"Director with ID {movie_data['director_id']} not found")
        
        # Create movie
        movie = Movie(**movie_data)
        
        # Add actors
        if actor_ids:
            actors = db.query(Actor).filter(Actor.id.in_(actor_ids)).all()
            if len(actors) != len(actor_ids):
                return error_response("One or more actor IDs not found", 404)
            movie.actors.extend(actors)
        
        # Add genres
        if genre_ids:
            genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            if len(genres) != len(genre_ids):
                return error_response("One or more genre IDs not found", 404)
            movie.genres.extend(genres)
        
        db.add(movie)
        db.commit()
        db.refresh(movie)
        
        movie_response = {
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
        
        return created_response(
            data=movie_response,
            message="Movie created successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error creating movie: {str(e)}", 500)
    
    finally:
        db.close()


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
    db = SessionLocal()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        
        if not movie:
            return not_found_response(f"Movie with ID {movie_id} not found")
        
        data = request.get_json()
        movie_schema = MovieUpdate(**data)
        
        # Extract relationship IDs
        update_data = movie_schema.model_dump(exclude_unset=True, exclude={'actor_ids', 'genre_ids'})
        
        # Validate director if updating
        if 'director_id' in update_data and update_data['director_id']:
            director = db.query(Director).filter(Director.id == update_data['director_id']).first()
            if not director:
                return not_found_response(f"Director with ID {update_data['director_id']} not found")
        
        # Update basic fields
        for key, value in update_data.items():
            setattr(movie, key, value)
        
        # Update actors if provided
        if movie_schema.actor_ids is not None:
            actors = db.query(Actor).filter(Actor.id.in_(movie_schema.actor_ids)).all()
            if len(actors) != len(movie_schema.actor_ids):
                return error_response("One or more actor IDs not found", 404)
            movie.actors.clear()
            movie.actors.extend(actors)
        
        # Update genres if provided
        if movie_schema.genre_ids is not None:
            genres = db.query(Genre).filter(Genre.id.in_(movie_schema.genre_ids)).all()
            if len(genres) != len(movie_schema.genre_ids):
                return error_response("One or more genre IDs not found", 404)
            movie.genres.clear()
            movie.genres.extend(genres)
        
        db.commit()
        db.refresh(movie)
        
        movie_response = {
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
        
        return success_response(
            data=movie_response,
            message="Movie updated successfully"
        )
    
    except ValidationError as e:
        return validation_error_response(e.errors())
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error updating movie: {str(e)}", 500)
    
    finally:
        db.close()


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
    db = SessionLocal()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        
        if not movie:
            return not_found_response(f"Movie with ID {movie_id} not found")
        
        db.delete(movie)
        db.commit()
        
        return success_response(
            data={"id": movie_id},
            message="Movie deleted successfully"
        )
    
    except Exception as e:
        db.rollback()
        return error_response(f"Error deleting movie: {str(e)}", 500)
    
    finally:
        db.close()