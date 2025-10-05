# Movie Explorer Platform

A full-stack web application that allows film enthusiasts to explore movies, actors, directors, and genres.

## 🎬 Project Overview

Movie Explorer Platform is a comprehensive movie database application where users can:
- Browse and search through a collection of movies
- Filter movies by genre, director, release year, or actor
- View detailed information about movies including cast, director, and ratings
- Explore actor and director profiles with their filmography
- Save favorite movies to a watch later list

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy with Pydantic validation
- **API Documentation:** Swagger/OpenAPI
- **Testing:** pytest
- **Linting:** pylint/flake8

### Frontend
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **UI Library:** Material-UI (MUI)
- **HTTP Client:** Axios
- **Routing:** React Router
- **Testing:** Jest + React Testing Library
- **Linting:** ESLint + Prettier

### DevOps
- **Containerization:** Docker & Docker Compose
- **Version Control:** Git

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **PostgreSQL** (v14 or higher)
- **Docker** and **Docker Compose** (optional, for containerized setup)
- **Git**

## 🚀 Getting Started

Detailed setup instructions can be found in separate setup_instructions.md

### With Docker (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd movie-explorer-platform

# Build and run with Docker Compose
docker-compose up --build
```

### Without Docker
Instructions for local setup will be provided in subsequent updates.

## 📁 Project Structure

```
movie-explorer-platform/
├── backend/                 # Flask backend application
├── frontend/               # React frontend application
├── docker-compose.yml      # Docker Compose configuration
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🧪 Running Tests

Test instructions will be added as the project develops.

## 📚 API Documentation

Once the backend is set up, API documentation will be available at:
- Swagger UI: `http://localhost:5000/api/docs`

## 🤝 Contributing

This is an assignment project. Contributions are not expected.

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Built as part of a Full Stack Development assignment.

---

**Status:** 🚧 Under Development

**Last Updated:** October 2025