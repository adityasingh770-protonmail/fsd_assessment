# Backend - Movie Explorer Platform

Flask-based REST API for the Movie Explorer Platform.

## Structure

```
backend/
├── app.py                 # Application entry point
├── config.py             # Configuration management
├── database.py           # Database connection and session management
├── requirements.txt      # Python dependencies
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas for validation
├── routes/              # API route handlers (blueprints)
├── services/            # Business logic layer
├── tests/               # Unit and integration tests
└── seed_data.py         # Database seeding script
```

## Setup Instructions

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5001`

## API Documentation

Once running, visit `http://localhost:5001/api/docs` for Swagger documentation.

## Testing

Run tests with:
```bash
pytest
```

With coverage:
```bash
pytest --cov=. --cov-report=html
```

## Linting

Check code quality:
```bash
pylint **/*.py
```