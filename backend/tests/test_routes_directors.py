"""
Tests for director routes.
"""
import pytest
import json


class TestDirectorsRoutes:
    """Test cases for director endpoints."""
    
    def test_get_directors(self, client):
        """Test getting all directors."""
        response = client.get('/api/v1/directors')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
    
    def test_get_directors_with_pagination(self, client):
        """Test directors pagination."""
        response = client.get('/api/v1/directors?page=1&page_size=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['meta']['page'] == 1
    
    def test_get_director_not_found(self, client):
        """Test getting non-existent director."""
        response = client.get('/api/v1/directors/99999')
        assert response.status_code == 404
    
    def test_create_director_success(self, client):
        """Test creating a director successfully."""
        director_data = {
            "name": "New Test Director",
            "bio": "A new test director",
            "birth_date": "1970-01-01",
            "nationality": "British"
        }
        
        response = client.post(
            '/api/v1/directors',
            data=json.dumps(director_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == director_data['name']
    
    def test_create_director_missing_name(self, client):
        """Test creating director without name."""
        director_data = {
            "bio": "Test bio"
        }
        
        response = client.post(
            '/api/v1/directors',
            data=json.dumps(director_data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_update_director_not_found(self, client):
        """Test updating non-existent director."""
        director_data = {"name": "Updated Name"}
        
        response = client.put(
            '/api/v1/directors/99999',
            data=json.dumps(director_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_director_not_found(self, client):
        """Test deleting non-existent director."""
        response = client.delete('/api/v1/directors/99999')
        assert response.status_code == 404