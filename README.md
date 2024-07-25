# Spotify Analyser

This project is a Django-based application for analyzing Spotify data.

It includes configurations for both development and production environments using Docker.

## Project Structure

```
SpotifyAnalyser/
├── backend/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── views.py
│   ├── templates/
│   │   ├── users/
│   │   │   ├── register.html
│   │   │   ├── login.html
│   │   │   ├── profile.html
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile.dev
│   ├── Dockerfile.prod
│   ├── init-db.sh
│   ├── .local.env
│   ├── .env.prod
│   ├── .pre-commit-config.yaml
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

## Prerequisites

- Docker
- Docker Compose
- Python (for setting up pre-commit hooks)

## Development Setup

### Configuration

- **Docker Compose**: `docker-compose.yml`
- **Dockerfile**: `backend/Dockerfile.dev`
- **Environment Variables**: `backend/.local.env`
- **Pre-commit Hooks**: `backend/.pre-commit-config.yaml`

### Environment Variables

Create a `.local.env` file in the `backend` directory with the following content:

```env
# DATABASE
POSTGRES_DB=spotify_analyser_db_name
POSTGRES_USER=spotify_analyser_db_user
POSTGRES_PASSWORD=password
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432

# DJANGO
DEBUG=True
SECRET_KEY=dev_secret_key
ALLOWED_HOSTS=*
LANGUAGE_CODE="en-GB"

# EMAIL
EMAIL_HOST="localhost"
EMAIL_PORT=25
EMAIL_HOST_PASSWORD=""
EMAIL_HOST_USER=""
EMAIL_USE_TLS=False
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
- **Environment Variables**: `backend/.prod.env`

### Environment Variables

Create a `.prod.env` file in the `backend` directory with the following content:

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

## User Management

### Registration

Users can register via the registration form:

- URL: `/users/register/`
- Template: `users/register.html`

### Login

Users can log in via the login form:

- URL: `/users/login/`
- Template: `users/login.html`

### Profile

Logged-in users can view their profile:

- URL: `/users/profile/`
- Template: `users/profile.html`
