"""
Utility functions for creating standardized API responses.
Ensures consistent response format across all endpoints.
"""
from typing import Any, Optional, Dict
from flask import jsonify


def success_response(
    data: Any,
    message: Optional[str] = None,
    status_code: int = 200,
    meta: Optional[Dict] = None
) -> tuple:
    """
    Create a success response.
    
    Args:
        data: Response data (can be dict, list, or any JSON-serializable object)
        message: Optional success message
        status_code: HTTP status code (default: 200)
        meta: Optional metadata (pagination info, etc.)
        
    Returns:
        tuple: (JSON response, status code)
        
    Example:
        return success_response(
            data=movies,
            message="Movies retrieved successfully",
            meta={"total": 100, "page": 1}
        )
    """
    response = {
        "success": True,
        "data": data
    }
    
    if message:
        response["message"] = message
    
    if meta:
        response["meta"] = meta
    
    return jsonify(response), status_code


def error_response(
    message: str,
    status_code: int = 400,
    errors: Optional[Dict] = None
) -> tuple:
    """
    Create an error response.
    
    Args:
        message: Error message
        status_code: HTTP status code (default: 400)
        errors: Optional detailed error information
        
    Returns:
        tuple: (JSON response, status code)
        
    Example:
        return error_response(
            message="Validation failed",
            status_code=400,
            errors={"title": "Title is required"}
        )
    """
    response = {
        "success": False,
        "error": message,
        "status": status_code
    }
    
    if errors:
        response["errors"] = errors
    
    return jsonify(response), status_code


def paginated_response(
    data: list,
    page: int,
    page_size: int,
    total_items: int,
    message: Optional[str] = None
) -> tuple:
    """
    Create a paginated response.
    
    Args:
        data: List of items for current page
        page: Current page number (1-indexed)
        page_size: Number of items per page
        total_items: Total number of items across all pages
        message: Optional message
        
    Returns:
        tuple: (JSON response, status code)
        
    Example:
        return paginated_response(
            data=movies,
            page=1,
            page_size=20,
            total_items=150
        )
    """
    total_pages = (total_items + page_size - 1) // page_size
    
    meta = {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }
    
    return success_response(data=data, message=message, meta=meta)


def created_response(
    data: Any,
    message: str = "Resource created successfully"
) -> tuple:
    """
    Create a 201 Created response.
    
    Args:
        data: Created resource data
        message: Success message
        
    Returns:
        tuple: (JSON response, status code)
    """
    return success_response(data=data, message=message, status_code=201)


def no_content_response() -> tuple:
    """
    Create a 204 No Content response.
    
    Returns:
        tuple: (Empty response, status code)
    """
    return '', 204


def not_found_response(message: str = "Resource not found") -> tuple:
    """
    Create a 404 Not Found response.
    
    Args:
        message: Error message
        
    Returns:
        tuple: (JSON response, status code)
    """
    return error_response(message=message, status_code=404)


def validation_error_response(errors: Dict) -> tuple:
    """
    Create a 422 Unprocessable Entity response for validation errors.
    
    Args:
        errors: Dictionary of validation errors
        
    Returns:
        tuple: (JSON response, status code)
        
    Example:
        return validation_error_response({
            "title": "Title must be at least 1 character",
            "release_year": "Release year must be between 1888 and 2100"
        })
    """
    return error_response(
        message="Validation failed",
        status_code=422,
        errors=errors
    )


def unauthorized_response(message: str = "Unauthorized") -> tuple:
    """
    Create a 401 Unauthorized response.
    
    Args:
        message: Error message
        
    Returns:
        tuple: (JSON response, status code)
    """
    return error_response(message=message, status_code=401)


def forbidden_response(message: str = "Forbidden") -> tuple:
    """
    Create a 403 Forbidden response.
    
    Args:
        message: Error message
        
    Returns:
        tuple: (JSON response, status code)
    """
    return error_response(message=message, status_code=403)


def server_error_response(
    message: str = "Internal server error"
) -> tuple:
    """
    Create a 500 Internal Server Error response.
    
    Args:
        message: Error message
        
    Returns:
        tuple: (JSON response, status code)
    """
    return error_response(message=message, status_code=500)