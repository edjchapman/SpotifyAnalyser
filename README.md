# Spotify Analyser

This project is a Django-based application for analyzing Spotify data.

It includes configurations for both development and production environments using Docker.

## Project Structure

```
myproject/
├── backend/
│   ├── myproject/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile.dev
│   ├── Dockerfile.prod
│   ├── init-db.sh
│   ├── .local.env
│   ├── .env.prod
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

## Prerequisites

- Docker
- Docker Compose

## Development Setup

### Configuration

- **Docker Compose**: `docker-compose.yml`
- **Dockerfile**: `backend/Dockerfile.dev`
- **Environment Variables**: `backend/.local.env`

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
SECRET_KEY=GFXkBxaxtnSEnDc9LTj85qhX4hEsifx8kFSrgqmq
ALLOWED_HOSTS=*
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  db:
    image: postgres:16.3
    volumes:
      - postgres_data:/var/lib/postgresql/data/
      - ./backend/init-db.sh:/docker-entrypoint-initdb.d/init-db.sh:ro
    ports:
      - "5432:5432"
    env_file:
      - ./backend/.local.env

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/backend
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - ./backend/.local.env

volumes:
  postgres_data:
```

### Dockerfile for Development

```dockerfile
# backend/Dockerfile.dev

FROM python:3.12.4-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY requirements.txt /backend/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /backend/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Initialization Script

```sh
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$POSTGRES_USER') THEN
            CREATE ROLE $POSTGRES_USER WITH LOGIN PASSWORD '$POSTGRES_PASSWORD';
        END IF;
    END
    \$\$;

    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB') THEN
            CREATE DATABASE $POSTGRES_DB;
        END IF;
    END
    \$\$;

    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL
```

### Running the Development Environment

```sh
docker-compose build
docker-compose up
```

## Production Setup

### Configuration

- **Docker Compose**: `docker-compose.prod.yml`
- **Dockerfile**: `backend/Dockerfile.prod`
- **Environment Variables**: `backend/.env.prod`

### Environment Variables

Create a `.env.prod` file in the `backend` directory with the following content:

```env
# DATABASE
POSTGRES_DB=spotify_analyser_db_name
POSTGRES_USER=spotify_analyser_db_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432

# DJANGO
DEBUG=False
SECRET_KEY=your_production_secret_key
ALLOWED_HOSTS=your_production_domain.com
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  db:
    image: postgres:16.3
    volumes:
      - postgres_data:/var/lib/postgresql/data/
      - ./backend/init-db.sh:/docker-entrypoint-initdb.d/init-db.sh:ro
    ports:
      - "5432:5432"
    env_file:
      - ./backend/.env.prod

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/backend
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - ./backend/.env.prod

volumes:
  postgres_data:
```

### Dockerfile for Production

```dockerfile
# backend/Dockerfile.prod

FROM python:3.12.4-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY requirements.txt /backend/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /backend/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Running the Production Environment

```sh
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

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
