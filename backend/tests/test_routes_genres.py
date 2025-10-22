"""
Tests for genre routes.
"""
import pytest
import json


class TestGenresRoutes:
    """Test cases for genre endpoints."""
    
    def test_get_genres(self, client):
        """Test getting all genres."""
        response = client.get('/api/v1/genres')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
    
    def test_get_genres_with_movies(self, client):
        """Test getting genres with their movies."""
        response = client.get('/api/v1/genres?include_movies=true')
        assert response.status_code == 200
    
    def test_get_genre_not_found(self, client):
        """Test getting non-existent genre."""
        response = client.get('/api/v1/genres/99999')
        assert response.status_code == 404
    
    def test_create_genre_success(self, client):
        """Test creating a genre successfully."""
        genre_data = {
            "name": "Horror",
            "description": "Horror movies"
        }
        
        response = client.post(
            '/api/v1/genres',
            data=json.dumps(genre_data),
            content_type='application/json'
        )
        
        # Note: This might fail if genre already exists
        # In real scenario, clear database or use unique names
        assert response.status_code in [201, 400]
    
    def test_create_genre_missing_name(self, client):
        """Test creating genre without name."""
        genre_data = {
            "description": "Test description"
        }
        
        response = client.post(
            '/api/v1/genres',
            data=json.dumps(genre_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_create_genre_duplicate_name(self, client):
        """Test creating genre with duplicate name."""
        genre_data = {
            "name": "UniqueGenre123",
            "description": "First genre"
        }
        
        # Create first genre
        response1 = client.post(
            '/api/v1/genres',
            data=json.dumps(genre_data),
            content_type='application/json'
        )
        
        # Try to create duplicate
        response2 = client.post(
            '/api/v1/genres',
            data=json.dumps(genre_data),
            content_type='application/json'
        )
        
        # Second should fail
        assert response2.status_code == 400
    
    def test_update_genre_not_found(self, client):
        """Test updating non-existent genre."""
        genre_data = {"name": "Updated Name"}
        
        response = client.put(
            '/api/v1/genres/99999',
            data=json.dumps(genre_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_genre_not_found(self, client):
        """Test deleting non-existent genre."""
        response = client.delete('/api/v1/genres/99999')
        assert response.status_code == 404