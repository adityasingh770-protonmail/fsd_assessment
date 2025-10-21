"""
Custom validation utilities for the application.
Contains reusable validation functions for common use cases.
"""
from datetime import datetime
from typing import Optional


def validate_year(year: int) -> bool:
    """
    Validate a year value for movies.
    
    Args:
        year: Year to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Note:
        Movies started around 1888, and we allow up to 5 years in the future
    """
    current_year = datetime.now().year
    return 1888 <= year <= current_year + 5


def validate_rating(rating: float) -> bool:
    """
    Validate a rating value (0-10 scale).
    
    Args:
        rating: Rating to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return 0.0 <= rating <= 10.0


def validate_page_number(page: int) -> bool:
    """
    Validate page number for pagination.
    
    Args:
        page: Page number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return page >= 1


def validate_page_size(size: int, max_size: int = 100) -> bool:
    """
    Validate page size for pagination.
    
    Args:
        size: Page size to validate
        max_size: Maximum allowed page size
        
    Returns:
        bool: True if valid, False otherwise
    """
    return 1 <= size <= max_size


def sanitize_search_query(query: Optional[str]) -> Optional[str]:
    """
    Sanitize search query string.
    
    Args:
        query: Search query to sanitize
        
    Returns:
        str: Sanitized query or None
    """
    if not query:
        return None
    
    # Strip whitespace and limit length
    sanitized = query.strip()[:200]
    
    return sanitized if sanitized else None


def validate_id(id_value: any) -> bool:
    """
    Validate an ID value.
    
    Args:
        id_value: ID to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        id_int = int(id_value)
        return id_int > 0
    except (ValueError, TypeError):
        return False


def normalize_string(value: Optional[str]) -> Optional[str]:
    """
    Normalize a string value by trimming whitespace.
    
    Args:
        value: String to normalize
        
    Returns:
        str: Normalized string or None
    """
    if not value:
        return None
    
    normalized = value.strip()
    return normalized if normalized else None