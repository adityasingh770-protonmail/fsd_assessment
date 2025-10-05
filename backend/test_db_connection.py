#!/usr/bin/env python
"""
Database connection test script.
Run this to verify database connection is working properly.

Usage:
    python test_db_connection.py
"""
from sqlalchemy import text
from database import engine, SessionLocal
from config import get_config


def test_connection():
    """Test basic database connection."""
    print("Testing database connection...")
    print("-" * 60)
    
    config = get_config()
    
    # Display connection info (hide password)
    db_uri = config.SQLALCHEMY_DATABASE_URI
    safe_uri = db_uri.replace(config.DB_PASSWORD, '****')
    print(f"Database URI: {safe_uri}")
    print()
    
    try:
        # Test engine connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print("✓ Engine connection successful")
            print(f"PostgreSQL version: {version}")
            print()
        
        # Test session
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print("✓ Session connection successful")
            print(f"Connected to database: {db_name}")
            print()
        finally:
            db.close()
        
        # Test connection pool
        print(f"✓ Connection pool configured")
        print(f"Pool size: {engine.pool.size()}")
        print()
        
        print("=" * 60)
        print("✓ All database connection tests passed!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print("✗ Database connection failed!")
        print(f"Error: {e}")
        print()
        print("Troubleshooting steps:")
        print("1. Ensure PostgreSQL is running:")
        print("   - macOS: brew services start postgresql")
        print("   - Linux: sudo systemctl start postgresql")
        print("   - Windows: Start PostgreSQL service")
        print()
        print("2. Create database if it doesn't exist:")
        print(f"   createdb {config.DB_NAME}")
        print()
        print("3. Verify credentials in .env file:")
        print(f"   DB_HOST={config.DB_HOST}")
        print(f"   DB_PORT={config.DB_PORT}")
        print(f"   DB_NAME={config.DB_NAME}")
        print(f"   DB_USER={config.DB_USER}")
        print("   DB_PASSWORD=<your-password>")
        return False


if __name__ == '__main__':
    import sys
    success = test_connection()
    sys.exit(0 if success else 1)