"""
Main application entry point for Movie Explorer Platform.
Initializes Flask app, configures extensions, and registers blueprints.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from config import get_config


def create_app(config_name=None):
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name:
        app.config.from_object(config_name)
    else:
        app.config.from_object(get_config())
    
    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Setup Swagger UI
    setup_swagger(app)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'movie-explorer-api',
            'version': app.config.get('API_VERSION', 'v1')
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information."""
        return jsonify({
            'message': 'Movie Explorer Platform API',
            'version': app.config.get('API_VERSION', 'v1'),
            'docs': '/api/docs',
            'health': '/health'
        }), 200
    
    return app


def register_blueprints(app):
    """Register Flask blueprints for API routes."""
    from routes import movies_bp, actors_bp, directors_bp, genres_bp
    
    api_prefix = app.config['API_PREFIX']
    
    app.register_blueprint(movies_bp, url_prefix=f"{api_prefix}/movies")
    app.register_blueprint(actors_bp, url_prefix=f"{api_prefix}/actors")
    app.register_blueprint(directors_bp, url_prefix=f"{api_prefix}/directors")
    app.register_blueprint(genres_bp, url_prefix=f"{api_prefix}/genres")


def register_error_handlers(app):
    """Register custom error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status': 500
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'error': 'Bad Request',
            'message': str(error),
            'status': 400
        }), 400


def setup_swagger(app):
    """Configure Swagger UI for API documentation."""
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Movie Explorer Platform API",
            'version': app.config.get('API_VERSION', 'v1')
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5001,  # moved port to 5001 as 5000 was being used for another program
        debug=app.config['DEBUG']
    )