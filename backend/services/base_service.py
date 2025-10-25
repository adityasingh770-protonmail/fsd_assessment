"""
Base service with database session management.
Provides utilities for all service classes.
"""
from typing import Optional, Generator
from contextlib import contextmanager
from sqlalchemy.orm import Session
from database import SessionLocal


class BaseService:
    """
    Base service class with database session management.

    Services can either:
    1. Use auto-managed sessions (simple operations)
    2. Accept explicit sessions (complex transactions)
    """

    @staticmethod
    @contextmanager
    def get_db() -> Generator[Session, None, None]:
        """
        Context manager for database sessions.
        Automatically handles commit/rollback/close.

        Usage:
            with BaseService.get_db() as db:
                # do database operations
                # auto-commits on success, rolls back on error
        """
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def _get_session(db: Optional[Session] = None) -> tuple[Session, bool]:
        """
        Get database session - either use provided one or create new.

        Args:
            db: Optional existing session

        Returns:
            Tuple of (session, should_close)
            - session: The database session to use
            - should_close: Whether caller should close this session
        """
        if db is not None:
            # Use provided session, caller manages lifecycle
            return db, False
        else:
            # Create new session, caller should close it
            return SessionLocal(), True
