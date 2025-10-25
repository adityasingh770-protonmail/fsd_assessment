"""
Database configuration and session management for Movie Explorer Platform.
Handles SQLAlchemy engine creation, session factory, and base model class.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from config import get_config

# Load configuration
config = get_config()

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=config.SQLALCHEMY_ECHO
)

# Create session factory
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Get database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        with get_db() as db:
            movies = db.query(Movie).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    This should be called when setting up the database for the first time.
    """
    # Import all models here to ensure they are registered with Base
    from models import Movie, Actor, Director, Genre, movie_actors, movie_genres
    
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_db():
    """
    Drop all database tables.
    WARNING: This will delete all data. Use with caution!
    """
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")


def reset_db():
    """
    Reset database by dropping and recreating all tables.
    WARNING: This will delete all data!
    """
    drop_db()
    init_db()
    print("Database reset completed!")


# Event listener for SQLite foreign key support (if using SQLite for testing)
# @event.listens_for(engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     """
#     Enable foreign key support for SQLite connections.
#     This is automatically called for each new connection.
#     """
#     if 'sqlite' in config.SQLALCHEMY_DATABASE_URI:
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON")
#         cursor.close()


# Context manager for database sessions
class DatabaseSession:
    """
    Context manager for database sessions.
    Ensures proper session cleanup and error handling.
    
    Example:
        with DatabaseSession() as db:
            movies = db.query(Movie).all()
    """
    
    def __enter__(self):
        """Enter the context manager."""
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager and handle cleanup."""
        if exc_type is not None:
            self.db.rollback()
        self.db.close()


# Export commonly used items
__all__ = [
    'engine',
    'SessionLocal',
    'Base',
    'get_db',
    'init_db',
    'drop_db',
    'reset_db',
    'DatabaseSession'
]