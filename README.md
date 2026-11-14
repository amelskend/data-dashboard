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