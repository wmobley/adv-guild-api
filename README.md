# Adventurer's Guild API

A FastAPI-based backend service for managing quests, campaigns, and user adventures in a gamified travel platform.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Overview

The Adventurer's Guild API provides a comprehensive backend for a travel quest platform where users can create, discover, and embark on location-based adventures. The system supports user management, quest creation, campaign organization, and social features like bookmarking and rating.

## Features

- **User Management**: Registration, authentication, and profile management
- **Quest System**: Create and manage location-based quests with difficulty levels
- **Campaign Organization**: Group related quests into themed campaigns
- **Location Services**: Geographic data management with real-world inspirations
- **Social Features**: Quest bookmarking, rating, and sharing
- **RESTful API**: Comprehensive API with automatic documentation
- **Database Migrations**: Alembic-powered database version control

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**
- **PostgreSQL 13+**
- **Docker & Docker Compose** (recommended for development)
- **Git**

## Installation

### Option 1: Docker Development Environment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/adv-guild-api.git
   cd adv-guild-api
   ```

2. **Configure Docker Permissions (First-time setup)**
   If you've just installed Docker, you'll likely need to add your user to the `docker` group to run commands without `sudo`.
   ```bash
   sudo usermod -aG docker $USER
   ```
   **Important**: You must log out and log back in for this change to take effect.

3. **Create environment file**
   Copy the example environment file. For production, be sure to edit the values, especially `JWT_SECRET_KEY`.
   ```bash
   cp example.env .env
   ```

4. **Start the development environment (with live reload)**
   ```bash
   docker compose -f docker-compose.dev.yml up -d
   ```

5. **Start the production environment**
   ```bash
   docker compose up -d --build
   ```

### Option 2: Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/adv-guild-api.git
   cd adv-guild-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Install PostgreSQL and create database
   createdb quest_db
   createuser quest_user --pwprompt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://quest_user:quest_password@localhost:5432/quest_db

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
ENVIRONMENT=development
DEBUG=true
API_V1_STR=/api/v1

# CORS Settings
# For production, set this to your frontend domain(s), e.g., ["https://adv-guild.com", "https://www.adv-guild.com"]
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Optional: External Services
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
SENDGRID_API_KEY=your-sendgrid-api-key
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Required |
| `ENVIRONMENT` | Application environment | `development` |
| `DEBUG` | Enable debug mode | `false` |
| `API_V1_STR` | API version prefix | `/api/v1` |

## Database Setup

### Using Docker (Recommended)

The Docker Compose setup automatically handles database initialization.

```bash
docker compose up -d db
```

### Manual Setup

1. **Install and start PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # macOS with Homebrew
   brew install postgresql
   brew services start postgresql
   ```

2. **Create database and user**
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE quest_db;
   CREATE USER quest_user WITH PASSWORD 'quest_password';
   GRANT ALL PRIVILEGES ON DATABASE quest_db TO quest_user;
   \q
   ```

3. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

3. **Create the test database**
   The test suite requires a separate database.
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE quest_db_test;
   GRANT ALL PRIVILEGES ON DATABASE quest_db_test TO quest_user;
   \q
   ```

4. **Seed sample data (optional)**
   ```bash
   python scripts/seed_data.py
   ```

## Running the Application

### Using Docker Compose

```bash
# Start production services in background
docker compose up -d

# Start development services in background
docker compose -f docker-compose.dev.yml up -d

# View API logs (for either environment)
docker compose logs -f api

# Stop and remove containers
docker compose down
```

### Local Development

```bash
# Activate virtual environment
source venv/bin/activate

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Production

```bash
# Using Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

In a production environment, replace `http://localhost:8000` with your API's public URL (e.g., `https://api.adv-guild.com`).

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | User registration |
| `/api/v1/auth/login` | POST | User authentication |
| `/api/v1/quests/` | GET | List all quests |
| `/api/v1/quests/` | POST | Create new quest |
| `/api/v1/campaigns/` | GET | List all campaigns |
| `/api/v1/locations/` | GET | List all locations |
| `/api/v1/users/me` | GET | Get current user profile |

## Development

### Project Structure

```
adv-guild-api/
├── app/
│   ├── api/                 # API route handlers
│   ├── core/                # Core functionality (config, security)
│   ├── db/                  # Database models and connection
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic
│   └── main.py              # FastAPI application
├── alembic/                 # Database migrations
├── data/                    # Sample data files
├── scripts/                 # Utility scripts
├── tests/                   # Test files
├── docker-compose.yml       # Docker services
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

### Adding New Dependencies

```bash
# Add new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# For Docker development
docker compose build api
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_quests.py

# Run with verbose output
pytest -v
```

### Test Database

Tests use a separate test database. Configure it in your `.env.test` file:

```env
DATABASE_URL=postgresql://quest_user:quest_password@localhost:5432/quest_test_db
```

## Deployment

### Docker Production Build

```bash
# Build production image
docker build -t adv-guild-api:latest .

# Run production container
docker run -d \
  --name adv-guild-api \
  -p 8000:8000 \
  --env-file .env.prod \
  adv-guild-api:latest
```

### Environment-Specific Configurations

Create separate environment files for different stages:

- `.env.development` - Local development
- `.env.staging` - Staging environment
- `.env.production` - Production environment

### Health Checks

The API includes health check endpoints:

- `/health` - Basic health check
- `/health/db` - Database connectivity check

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   pytest
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black app/
isort app/

# Run linting
flake8 app/
mypy app/
```

## Troubleshooting

### Common Issues

**Database Connection Issues**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
psql -h localhost -U quest_user -d quest_db
```

**Migration Issues**
```bash
# Reset migrations (development only)
alembic downgrade base
alembic upgrade head
```

**Docker Issues**
```bash
# Rebuild containers
docker compose down
docker compose build --no-cache
docker compose up
```

### Logs

```bash
# Docker logs
docker compose logs -f api

# Application logs (if running locally)
tail -f logs/app.log
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

**Happy Adventuring!** 🗺️⚔️