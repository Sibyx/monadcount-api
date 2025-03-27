# Changelog

This changelog suppose to follow rules defined in the [changelog.md](https://changelog.md)

## 0.3.0

- **Added**: `Experiment` model introduced (to gather data also from simulations)
- **Changed**: Migrating `enums`

## 0.2.0 - 2024-11-26

- **Added**: `Structure` database table
- **Added**: `UploadedFile.filesize` column with related CLI tools

## 0.1.0 - 2024-11-23 (Leibniz release)

Initial release dedicated to the Gottfried Wilhelm Leibniz and his monadology which inspired the name of this project.

- **Added**: Sync API (HTTP based)
- **Added**: Measurement parsers
- **Added**: Dramatiq workers
- **Added**: Clickhouse measurement storage
- **Added**: PostgreSQL + TimescaleDB + PostGIS for relational data
- **Added**: Grafana support
