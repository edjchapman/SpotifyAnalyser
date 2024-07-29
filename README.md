# Spotify Analyser

This project is a Django-based application for analyzing Spotify data.

It includes configurations for both development and production environments using Docker.

---

## Project Structure

```
SpotifyAnalyser/
├── backend/
│ ├── core/
│ │ ├── __init__.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── wsgi.py
│ ├── accounts/
│ │ ├── __init__.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── forms.py
│ │ ├── models.py
│ │ ├── tests.py
│ │ ├── views.py
│ │ ├── urls.py
│ │ ├── templates/
│ │ │ ├── accounts/
│ │ │ │ ├── register.html
│ │ │ │ ├── login.html
│ │ │ │ ├── profile.html
│ ├── spotify/
│ │ ├── __init__.py
│ │ ├── admin.py
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── urls.py
│ │ ├── services.py
│ │ ├── tests.py
│ ├── templates/
│ │ ├── base.html
│ ├── static/
│ │ ├── css/
│ │ │ ├── styles.css
│ ├── manage.py
│ ├── requirements.txt
│ ├── Dockerfile.dev
│ ├── Dockerfile.prod
│ ├── init-db.sh
│ ├── .local.env
│ ├── .prod.env
│ ├── .env # This file is not committed to git
│ ├── .pre-commit-config.yaml
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

---

## Prerequisites

- Docker
- Docker Compose
- Python (for setting up pre-commit hooks)
- Spotify API credentials (Client ID and Client Secret)
  from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Development Setup

### Configuration

- **Docker Compose**: `docker-compose.yml`
- **Dockerfile**: `backend/Dockerfile.dev`
- **Environment Variables**: `backend/.local.env`
- **Pre-commit Hooks**: `backend/.pre-commit-config.yaml`

### Setting Up Environment Variables

Create a `backend/.env` file in the `backend` directory by copying from `backend/.local.env`
and populating it with your actual API keys and secrets:

```sh
cp backend/.local.env backend/.env
# Then edit backend/.env to add your real values
```

### Pre-commit Hooks Setup

1. **Install pre-commit**:

    ```sh
    pip install pre-commit
    ```

2. **Install the pre-commit hooks**:

    ```sh
    pre-commit install
    ```

3. **Run pre-commit manually (optional)**:

    ```sh
    pre-commit run --all-files
    ```

### Running the Development Environment

```sh
docker-compose build
docker-compose up
```

---

## Production Setup

### Configuration

- **Docker Compose**: `docker-compose.prod.yml`
- **Dockerfile**: `backend/Dockerfile.prod`
- **Environment Variables**: `backend/.env`

### Setting Up Environment Variables

Create a `backend/.env` file in the `backend` directory with the following content:

```env
# DATABASE
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_DB_HOST=db.prod.com
POSTGRES_DB_PORT=5432

# DJANGO
DEBUG=False
SECRET_KEY=prod_secret_key
ALLOWED_HOSTS=prod.com,sub.prod.com
LANGUAGE_CODE="en-GB"

# EMAIL
EMAIL_HOST="email.prod.com"
EMAIL_PORT=25
EMAIL_HOST_PASSWORD=""
EMAIL_HOST_USER=""
EMAIL_USE_TLS=False

# SPOTIFY
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=https://your-production-url.com/spotify/callback/
```

### Running the Production Environment

```sh
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

---

## Common Commands

- **Build the Docker images**:
  ```sh
  docker-compose build
  ```

- **Start the services**:
  ```sh
  docker-compose up
  ```

- **Stop the services**:
  ```sh
  docker-compose down
  ```

- **Run database migrations**:
  ```sh
  docker-compose exec backend python manage.py migrate
  ```

- **Create a superuser**:
  ```sh
  docker-compose exec backend python manage.py createsuperuser
  ```

- **View logs**:
  ```sh
  docker-compose logs
  ```

---

## User Management

### Registration

Users can register via the registration form:

- URL: `/accounts/register/`
- Template: `accounts/register.html`

### Login

Users can log in via the login form:

- URL: `/accounts/login/`
- Template: `accounts/login.html`

### Profile

Logged-in users can view their profile:

- URL: `/accounts/profile/`
- Template: `accounts/profile.html`

---

## Running Tests

### Test Files

- `backend/accounts/tests.py`
- `backend/spotify/tests.py`

### Running Tests

To run tests, use the following command:

```sh
docker-compose exec backend python manage.py test
```

---

Make sure to replace the placeholder values in the `.env` file with your actual Spotify API credentials
and other configuration details.