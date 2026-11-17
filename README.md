# CMDB Assets Dashboard

Full-stack application designed to manage and visualize infrastructure assets.

## Features

- REST API built with FastAPI
- PostgreSQL database
- Infrastructure asset management
- CSV import and processing with Pandas
- S3-compatible object storage
- Svelte frontend
- Tailwind CSS + DaisyUI UI components
- Dockerized development environment
- GitLab CI/CD pipeline
- Unit tests with Pytest

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pandas

### Frontend
- Svelte
- Tailwind CSS
- DaisyUI

### DevOps
- Docker
- GitLab CI/CD

### Storage
- S3-compatible storage (MinIO)

## Local development with Docker

Create a `.env` file at the project root with the PostgreSQL and MinIO
credentials, then start the services:

```bash
docker compose up --build
```

MinIO is available at `http://localhost:9001`. The `minio-init` service creates
the `datasets` bucket before the backend starts. The backend uses
`http://minio:9000` internally; `localhost:9000` is only for tools running on
the host machine.

## Architecture

Frontend (Svelte)
↓
REST API (FastAPI)
↓
PostgreSQL

CSV Imports
↓
Pandas Processing
↓
S3 Storage