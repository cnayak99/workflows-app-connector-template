# Configuration Directory

This directory contains all configuration files for the application. Centralizing configuration files makes the codebase easier to maintain and navigate.

## Files in this directory

- `app_config.yaml` - Main application configuration
- `docker-compose.yml` - Docker Compose configuration
- `gunicorn_config.py` - Gunicorn web server configuration
- `.env` - Environment variables

## Usage

Configuration files in this directory are referenced from the main application code:

- `app_config.yaml` is loaded by `main.py`
- `gunicorn_config.py` is referenced in the Dockerfile
- `docker-compose.yml` is used by the `run_docker_compose.sh` script

To modify application configuration, edit the files in this directory rather than creating new configuration files in the root directory.
