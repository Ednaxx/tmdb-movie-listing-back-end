# TMDB Movie Listing - Back End

A FastAPI-based REST API for managing movie favorites using The Movie Database (TMDB) API. This application allows users to search for movies, manage their personal favorites list, and share their favorites with others via shareable links.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLModel (SQLAlchemy ORM)
- **Authentication**: JWT tokens with OAuth2 password flow
- **Password Hashing**: Argon2
- **External API**: TMDB (The Movie Database)
- **Python**: 3.11+

## API Endpoints

### Health Check
- `GET /health` - Check API status

### User Management
- `POST /users/register` - Register a new user
- `POST /users/token` - Login and get access token
- `POST /users/share-token` - Generate a shareable link for your favorites
- `DELETE /users/share-token` - Revoke your shareable link

### TMDB (requires authentication)
- `GET /tmdb/search?query={query}&page={page}` - Search movies
- `GET /tmdb/movie/{movie_id}` - Get movie details

### Favorites (requires authentication)
- `POST /favorites` - Add a movie to favorites
- `GET /favorites` - Get your favorite movies
- `DELETE /favorites/{tmdb_movie_id}` - Remove a movie from favorites
- `GET /favorites/shared/{share_token}` - View someone's shared favorites (public)

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- TMDB API Key (get one from [TMDB](https://www.themoviedb.org/settings/api))

## Installation

### Option 1: Local Setup (Standard Approach)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ednaxx/tmdb-movie-listing-back-end.git
   cd tmdb-movie-listing-back-end
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**
   - Install PostgreSQL on your system
   - Create a new database:
     ```sql
     CREATE DATABASE tmdb_movies;
     ```

5. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.template .env
   # Then edit the variables according to you environment.
   ```

6. **Run the application**
   ```bash
   fastapi dev app/main.py
   ```

   The API will be available at `http://localhost:8000`

### Option 2: Dev Container Setup (Recommended for VS Code)

This project includes a complete dev container configuration that sets up Python 3.11 and PostgreSQL automatically.

1. **Prerequisites**
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Install [Visual Studio Code](https://code.visualstudio.com/)
   - Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Clone the repository**
   ```bash
   git clone https://github.com/Ednaxx/tmdb-movie-listing-back-end.git
   cd tmdb-movie-listing-back-end
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.template .env
   # Then edit the variables according to you environment.
   ```

4. **Open in Dev Container**
   - Open the project folder in VS Code
   - Press `F1` and select `Dev Containers: Reopen in Container`
   - Wait for the container to build and start (first time takes a few minutes)
   - Dependencies will be installed automatically via `postCreateCommand`

5. **Run the application**
   
   Once inside the dev container, open a terminal and run:
   ```bash
   fastapi dev app/main.py
   ```

   The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI app initialization and configuration
├── config.py            # Settings and environment variables
├── db.py                # Database setup and session management
├── favorites/           # Favorites management
│   ├── models.py        # FavoriteMovie models
│   └── router.py        # Favorites endpoints
├── tmdb/                # TMDB API integration
│   ├── tmdb_client.py   # TMDB API client
│   └── tmdb_router.py   # TMDB endpoints
└── user/                # User management and authentication
    ├── auth.py          # JWT authentication utilities
    ├── models.py        # User models
    └── router.py        # User endpoints
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [TMDB API Documentation](https://developers.themoviedb.org/3)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
