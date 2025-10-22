"""
Tests for actor routes.
"""
import pytest
import json


class TestActorsRoutes:
    """Test cases for actor endpoints."""
    
    def test_get_actors(self, client):
        """Test getting all actors."""
        response = client.get('/api/v1/actors')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert 'meta' in data
    
    def test_get_actors_with_pagination(self, client):
        """Test actors pagination."""
        response = client.get('/api/v1/actors?page=1&page_size=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['meta']['page'] == 1
        assert data['meta']['page_size'] == 10
    
    def test_get_actors_with_movies(self, client):
        """Test getting actors with their movies."""
        response = client.get('/api/v1/actors?include_movies=true')
        assert response.status_code == 200
    
    def test_get_actor_not_found(self, client):
        """Test getting non-existent actor."""
        response = client.get('/api/v1/actors/99999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_create_actor_success(self, client):
        """Test creating an actor successfully."""
        actor_data = {
            "name": "New Test Actor",
            "bio": "A new test actor",
            "birth_date": "1990-01-01",
            "nationality": "American"
        }
        
        response = client.post(
            '/api/v1/actors',
            data=json.dumps(actor_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == actor_data['name']
    
    def test_create_actor_missing_name(self, client):
        """Test creating actor without name."""
        actor_data = {
            "bio": "Test bio",
            "nationality": "American"
        }
        
        response = client.post(
            '/api/v1/actors',
            data=json.dumps(actor_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_create_actor_empty_name(self, client):
        """Test creating actor with empty name."""
        actor_data = {
            "name": "   ",
            "bio": "Test bio"
        }
        
        response = client.post(
            '/api/v1/actors',
            data=json.dumps(actor_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_create_actor_future_birth_date(self, client):
        """Test creating actor with future birth date."""
        actor_data = {
            "name": "Test Actor",
            "birth_date": "2030-01-01"
        }
        
        response = client.post(
            '/api/v1/actors',
            data=json.dumps(actor_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_update_actor_not_found(self, client):
        """Test updating non-existent actor."""
        actor_data = {"name": "Updated Name"}
        
        response = client.put(
            '/api/v1/actors/99999',
            data=json.dumps(actor_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_actor_not_found(self, client):
        """Test deleting non-existent actor."""
        response = client.delete('/api/v1/actors/99999')
        assert response.status_code == 404