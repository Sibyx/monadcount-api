# MonadCount API Server

Welcome to the MonadCount API Server repository! This server is the backend component of the MonadCount project,
designed to collect and manage data from ESP32 sniffer devices. The project aims to elevate the simple act of
counting to a new philosophical dimension by drawing inspiration from Leibniz's concept of monads—indivisible units
that make up the universe.

## Overview

The MonadCount API Server is built using FastAPI, SQLModel, and integrates with PostgreSQL enhanced with TimescaleDB
and PostGIS for time-series and geospatial data capabilities. It provides endpoints for ESP32 devices to upload data
efficiently. The measurements collected by ESP32 sniffers are stored inside the Clickhouse database.

## Getting Started

### From scratch

```shell
# Clone the repository
git clone git@github.com:Sibyx/monadcount-api.git /monadcount-api

# Create environment and install dependencies
cd /monadcount-api
python -m venv .venv
source .venv/bin/active
poetry install

# Create configuration (edit the .env)
cp .env.example .env

# Run server
uvicorn main:app --reload
```

## Command Line Interface (CLI)

| Command                                            | Description                                                |
|----------------------------------------------------|------------------------------------------------------------|
| `python -m monadcount_api.cli import_measurements` | Import sniffer measurement file to PostgreSQL              |
| `python -m monadcount_api.cli enqueue`             | Add all `pending` `UploadedFile` object to the tasks queue |
| `python -m monadcount_api.cli openapi`             | Generates OpenAPI JSON Specification                       |


---
Created with ❤️ using ☕️for my cute kawaii PhD thesis on FIIT STU

If you enjoy using this project, consider donating! Your donations will go towards therapy sessions because
I'm an alcoholic and substance abuser and this is my cry for help. Cheers 🍻!
