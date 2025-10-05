# Complete Project Structure

This document outlines the complete directory structure for the Movie Explorer Platform.

```
movie-explorer-platform/
│
├── README.md                          # Main project documentation
├── .gitignore                         # Root gitignore
├── docker-compose.yml                 # Docker Compose configuration
├── PROJECT_STRUCTURE.md               # This file
│
├── backend/                           # Flask Backend
│   ├── .gitignore                     # Backend specific gitignore
│   ├── README.md                      # Backend documentation
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment variables template
│   ├── app.py                         # Application entry point
│   ├── config.py                      # Configuration management
│   ├── database.py                    # Database setup and connection
│   ├── seed_data.py                   # Database seeding script
│   ├── Dockerfile                     # Backend Docker configuration
│   │
│   ├── models/                        # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── movie.py                   # Movie model
│   │   ├── actor.py                   # Actor model
│   │   ├── director.py                # Director model
│   │   ├── genre.py                   # Genre model
│   │   └── associations.py            # Association tables
│   │
│   ├── schemas/                       # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── movie.py                   # Movie schemas
│   │   ├── actor.py                   # Actor schemas
│   │   ├── director.py                # Director schemas
│   │   └── genre.py                   # Genre schemas
│   │
│   ├── routes/                        # API Routes (Blueprints)
│   │   ├── __init__.py
│   │   ├── movies.py                  # Movie endpoints
│   │   ├── actors.py                  # Actor endpoints
│   │   ├── directors.py               # Director endpoints
│   │   └── genres.py                  # Genre endpoints
│   │
│   ├── services/                      # Business Logic
│   │   ├── __init__.py
│   │   ├── movie_service.py
│   │   ├── actor_service.py
│   │   ├── director_service.py
│   │   └── genre_service.py
│   │
│   ├── utils/                         # Utility Functions
│   │   ├── __init__.py
│   │   ├── response.py                # Response helpers
│   │   └── validators.py              # Custom validators
│   │
│   ├── tests/                         # Backend Tests
│   │   ├── __init__.py
│   │   ├── conftest.py                # Test configuration
│   │   ├── test_models.py
│   │   ├── test_routes.py
│   │   └── test_services.py
│   │
│   └── swagger/                       # Swagger Documentation
│       └── openapi.yaml               # OpenAPI specification
│
├── frontend/                          # React Frontend
│   ├── .gitignore                     # Frontend specific gitignore
│   ├── README.md                      # Frontend documentation
│   ├── package.json                   # Node dependencies
│   ├── package-lock.json
│   ├── .env.example                   # Environment variables template
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── tsconfig.node.json
│   ├── vite.config.ts                 # Vite configuration
│   ├── .eslintrc.cjs                  # ESLint configuration
│   ├── .prettierrc                    # Prettier configuration
│   ├── index.html                     # HTML entry point
│   ├── Dockerfile                     # Frontend Docker configuration
│   │
│   ├── public/                        # Static Assets
│   │   └── vite.svg
│   │
│   └── src/                           # Source Code
│       ├── main.tsx                   # Application entry
│       ├── App.tsx                    # Root component
│       ├── App.css
│       ├── index.css
│       ├── vite-env.d.ts
│       │
│       ├── components/                # Reusable Components
│       │   ├── Layout/
│       │   │   ├── Layout.tsx
│       │   │   ├── Navbar.tsx
│       │   │   └── Footer.tsx
│       │   ├── MovieCard/
│       │   │   ├── MovieCard.tsx
│       │   │   └── MovieCard.test.tsx
│       │   ├── MovieFilters/
│       │   │   ├── MovieFilters.tsx
│       │   │   └── MovieFilters.test.tsx
│       │   ├── ErrorBoundary/
│       │   │   └── ErrorBoundary.tsx
│       │   └── Loading/
│       │       └── LoadingSpinner.tsx
│       │
│       ├── pages/                     # Page Components
│       │   ├── MoviesList/
│       │   │   ├── MoviesList.tsx
│       │   │   └── MoviesList.test.tsx
│       │   ├── MovieDetail/
│       │   │   ├── MovieDetail.tsx
│       │   │   └── MovieDetail.test.tsx
│       │   ├── ActorProfile/
│       │   │   ├── ActorProfile.tsx
│       │   │   └── ActorProfile.test.tsx
│       │   ├── DirectorProfile/
│       │   │   ├── DirectorProfile.tsx
│       │   │   └── DirectorProfile.test.tsx
│       │   ├── Favorites/
│       │   │   ├── Favorites.tsx
│       │   │   └── Favorites.test.tsx
│       │   └── NotFound/
│       │       └── NotFound.tsx
│       │
│       ├── services/                  # API Services
│       │   ├── api.ts                 # API client setup
│       │   ├── movieService.ts
│       │   ├── actorService.ts
│       │   ├── directorService.ts
│       │   └── genreService.ts
│       │
│       ├── types/                     # TypeScript Types
│       │   ├── movie.ts
│       │   ├── actor.ts
│       │   ├── director.ts
│       │   ├── genre.ts
│       │   └── api.ts
│       │
│       ├── utils/                     # Utility Functions
│       │   ├── localStorage.ts
│       │   ├── formatters.ts
│       │   └── validators.ts
│       │
│       └── hooks/                     # Custom React Hooks
│           ├── useFavorites.ts
│           └── useDebounce.ts
│
└── docs/                              # Additional Documentation
    ├── API.md                         # API documentation
    ├── SETUP.md                       # Detailed setup guide
    └── ARCHITECTURE.md                # Architecture decisions
```

## Key Directory Purposes

### Backend
- **models/**: Database models using SQLAlchemy ORM
- **schemas/**: Request/response validation using Pydantic
- **routes/**: API endpoints organized as Flask blueprints
- **services/**: Business logic layer (keeps routes thin)
- **utils/**: Helper functions and utilities
- **tests/**: Comprehensive test suite

### Frontend
- **components/**: Reusable UI components (atomic design pattern)
- **pages/**: Full page components (container components)
- **services/**: API communication layer
- **types/**: TypeScript type definitions and interfaces
- **utils/**: Helper functions
- **hooks/**: Custom React hooks for shared logic

## File Naming Conventions

### Backend
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case()`

### Frontend
- Components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Types: `PascalCase` or `camelCase.ts`
- Tests: `*.test.tsx` or `*.spec.tsx`