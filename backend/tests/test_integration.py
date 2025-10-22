"""
Integration tests for complete workflows.
"""
import pytest
import json


class TestMovieWorkflow:
    """Test complete movie creation workflow."""
    
    def test_create_complete_movie_workflow(self, client):
        """Test creating a movie with all relationships."""
        
        import time
        unique_id = str(int(time.time() * 1000))  # Unique timestamp
        
        # Step 1: Create a director
        director_data = {
            "name": f"Workflow Director {unique_id}",
            "bio": "Test director for workflow",
            "nationality": "American"
        }
        director_response = client.post(
            '/api/v1/directors',
            data=json.dumps(director_data),
            content_type='application/json'
        )
        assert director_response.status_code == 201
        director_id = json.loads(director_response.data)['data']['id']
        
        # Step 2: Create actors
        actor1_data = {
            "name": f"Workflow Actor 1 {unique_id}",
            "bio": "First test actor"
        }
        actor1_response = client.post(
            '/api/v1/actors',
            data=json.dumps(actor1_data),
            content_type='application/json'
        )
        assert actor1_response.status_code == 201
        actor1_id = json.loads(actor1_response.data)['data']['id']
        
        actor2_data = {
            "name": f"Workflow Actor 2 {unique_id}",
            "bio": "Second test actor"
        }
        actor2_response = client.post(
            '/api/v1/actors',
            data=json.dumps(actor2_data),
            content_type='application/json'
        )
        assert actor2_response.status_code == 201
        actor2_id = json.loads(actor2_response.data)['data']['id']
        
        # Step 3: Create genres with unique names
        genre1_data = {
            "name": f"WorkflowGenre{unique_id}",
            "description": "First workflow genre"
        }
        genre1_response = client.post(
            '/api/v1/genres',
            data=json.dumps(genre1_data),
            content_type='application/json'
        )
        assert genre1_response.status_code == 201
        genre1_id = json.loads(genre1_response.data)['data']['id']
        
        # Step 4: Create movie with all relationships
        movie_data = {
            "title": "Workflow Test Movie",
            "description": "Complete workflow test",
            "release_year": 2024,
            "duration_minutes": 120,
            "rating": 8.5,
            "director_id": director_id,
            "actor_ids": [actor1_id, actor2_id],
            "genre_ids": [genre1_id]
        }
        movie_response = client.post(
            '/api/v1/movies',
            data=json.dumps(movie_data),
            content_type='application/json'
        )
        assert movie_response.status_code == 201
        movie_id = json.loads(movie_response.data)['data']['id']
        
        # Step 5: Verify movie has all relationships
        get_movie_response = client.get(f'/api/v1/movies/{movie_id}')
        assert get_movie_response.status_code == 200
        movie_detail = json.loads(get_movie_response.data)['data']
        
        assert movie_detail['director']['id'] == director_id
        assert len(movie_detail['actors']) == 2
        assert len(movie_detail['genres']) == 1
        
        # Step 6: Update movie
        update_data = {
            "rating": 9.0
        }
        update_response = client.put(
            f'/api/v1/movies/{movie_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        
        # Step 7: Verify update
        updated_movie = client.get(f'/api/v1/movies/{movie_id}')
        assert json.loads(updated_movie.data)['data']['rating'] == 9.0
        
        # Step 8: Delete movie
        delete_response = client.delete(f'/api/v1/movies/{movie_id}')
        assert delete_response.status_code == 200
        
        # Step 9: Verify deletion
        verify_response = client.get(f'/api/v1/movies/{movie_id}')
        assert verify_response.status_code == 404


class TestAPIHealthAndMeta:
    """Test API health and meta endpoints."""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'version' in data


class TestErrorHandling:
    """Test error handling across endpoints."""
    
    def test_404_for_invalid_route(self, client):
        """Test 404 for non-existent route."""
        response = client.get('/api/v1/invalid-route')
        assert response.status_code == 404
    
    def test_invalid_json_body(self, client):
        """Test handling of invalid JSON."""
        response = client.post(
            '/api/v1/movies',
            data='invalid json',
            content_type='application/json'
        )
        # Should return an error (400 or 422)
        assert response.status_code >= 400
    
    def test_missing_content_type(self, client):
        """Test POST without content type."""
        response = client.post(
            '/api/v1/movies',
            data=json.dumps({"title": "Test"})
        )
        assert response.status_code >= 400