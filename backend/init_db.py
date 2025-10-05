#!/usr/bin/env python
"""
Database initialization script.
Run this script to create database tables.

Usage:
    python init_db.py [--reset]
    
Options:
    --reset     Drop all tables before creating (WARNING: deletes all data)
"""
import sys
import argparse
from database import init_db, reset_db, engine
from sqlalchemy import inspect


def check_database_exists():
    """
    Check if database connection is successful.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Try to connect to the database
        with engine.connect() as connection:
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Database exists (create with: createdb movie_explorer)")
        print("3. Credentials in .env file are correct")
        return False


def check_tables_exist():
    """
    Check if database tables already exist.
    
    Returns:
        list: List of existing table names
    """
    inspector = inspect(engine)
    return inspector.get_table_names()


def main():
    """Main function to initialize database."""
    parser = argparse.ArgumentParser(
        description='Initialize Movie Explorer database'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset database (WARNING: deletes all data)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Movie Explorer Platform - Database Initialization")
    print("=" * 60)
    print()
    
    # Check database connection
    if not check_database_exists():
        sys.exit(1)
    
    # Check existing tables
    existing_tables = check_tables_exist()
    
    if existing_tables and not args.reset:
        print(f"\n⚠ Warning: Database already has {len(existing_tables)} tables:")
        for table in existing_tables:
            print(f"  - {table}")
        print("\nUse --reset flag to drop and recreate all tables")
        print("Example: python init_db.py --reset")
        sys.exit(0)
    
    # Initialize or reset database
    try:
        if args.reset:
            print("\n⚠ RESETTING DATABASE (all data will be lost)...")
            confirmation = input("Type 'yes' to confirm: ")
            if confirmation.lower() != 'yes':
                print("Database reset cancelled")
                sys.exit(0)
            reset_db()
        else:
            print("\nCreating database tables...")
            init_db()
        
        print("\n" + "=" * 60)
        print("✓ Database initialization completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run seed data script: python seed_data.py")
        print("2. Start the application: python app.py")
        
    except Exception as e:
        print(f"\n✗ Error during database initialization: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()