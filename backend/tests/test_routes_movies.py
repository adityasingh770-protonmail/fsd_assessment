"""
Tests for movie routes.
"""
import pytest
import json


class TestMoviesRoutes:
    """Test cases for movie endpoints."""
    
    def test_get_movies_empty(self, client):
        """Test getting movies when database is empty."""
        response = client.get('/api/v1/movies')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert 'meta' in data
    
    def test_get_movies_with_pagination(self, client):
        """Test movies pagination."""
        response = client.get('/api/v1/movies?page=1&page_size=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'meta' in data
        assert data['meta']['page'] == 1
        assert data['meta']['page_size'] == 10
    
    def test_get_movies_invalid_page(self, client):
        """Test movies with invalid page number."""
        response = client.get('/api/v1/movies?page=-1')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_get_movies_with_genre_filter(self, client):
        """Test filtering movies by genre."""
        response = client.get('/api/v1/movies?genre=Action')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_get_movies_with_director_filter(self, client):
        """Test filtering movies by director."""
        response = client.get('/api/v1/movies?director=Nolan')
        assert response.status_code == 200
    
    def test_get_movies_with_year_filter(self, client):
        """Test filtering movies by year."""
        response = client.get('/api/v1/movies?year=2020')
        assert response.status_code == 200
    
    def test_get_movies_with_rating_filter(self, client):
        """Test filtering movies by rating range."""
        response = client.get('/api/v1/movies?min_rating=8.0&max_rating=10.0')
        assert response.status_code == 200
    
    def test_get_movies_with_search(self, client):
        """Test searching movies."""
        response = client.get('/api/v1/movies?search=test')
        assert response.status_code == 200
    
    def test_get_movie_not_found(self, client):
        """Test getting non-existent movie."""
        response = client.get('/api/v1/movies/99999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not found' in data['error'].lower()
    
    def test_create_movie_success(self, client):
        """Test creating a movie successfully."""
        movie_data = {
            "title": "New Test Movie",
            "description": "A brand new test movie",
            "release_year": 2024,
            "duration_minutes": 120,
            "rating": 8.0
        }
        
        response = client.post(
            '/api/v1/movies',
            data=json.dumps(movie_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == movie_data['title']
    
    def test_create_movie_missing_title(self, client):
        """Test creating movie without title."""
        movie_data = {
            "release_year": 2024,
            "rating": 8.0
        }
        
        response = client.post(
            '/api/v1/movies',
            data=json.dumps(movie_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_create_movie_invalid_year(self, client):
        """Test creating movie with invalid year."""
        movie_data = {
            "title": "Test Movie",
            "release_year": 1800,
            "rating": 8.0
        }
        
        response = client.post(
            '/api/v1/movies',
            data=json.dumps(movie_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_create_movie_invalid_rating(self, client):
        """Test creating movie with invalid rating."""
        movie_data = {
            "title": "Test Movie",
            "release_year": 2024,
            "rating": 15.0
        }
        
        response = client.post(
            '/api/v1/movies',
            data=json.dumps(movie_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_update_movie_not_found(self, client):
        """Test updating non-existent movie."""
        movie_data = {"rating": 9.0}
        
        response = client.put(
            '/api/v1/movies/99999',
            data=json.dumps(movie_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_movie_not_found(self, client):
        """Test deleting non-existent movie."""
        response = client.delete('/api/v1/movies/99999')
        assert response.status_code == 404


class TestMovieFiltering:
    """Test cases for movie filtering functionality."""
    
    def test_filter_by_multiple_criteria(self, client):
        """Test filtering by multiple criteria."""
        response = client.get('/api/v1/movies?genre=Sci-Fi&min_rating=8.0&year=2020')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_search_in_title_and_description(self, client):
        """Test search functionality."""
        response = client.get('/api/v1/movies?search=inception')
        assert response.status_code == 200
    
    def test_pagination_with_filters(self, client):
        """Test pagination works with filters."""
        response = client.get('/api/v1/movies?genre=Action&page=1&page_size=5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'meta' in data


class TestMovieRelationships:
    """Test cases for movie relationships."""
    
    def test_create_movie_with_director(self, client):
        """Test creating movie with director."""
        # This test would need a director to exist first
        pass
    
    def test_create_movie_with_actors(self, client):
        """Test creating movie with actors."""
        # This test would need actors to exist first
        pass
    
    def test_create_movie_with_genres(self, client):
        """Test creating movie with genres."""
        # This test would need genres to exist first
        pass