# Page Analyzer
[![Actions Status](https://github.com/vitallcore/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vitallcore/python-project-83/actions)

## Description
Page Analyzer is a simple web application that checks the basic page-level elements of websites valuable for on-page SEO.

## Installation
Clone this repository to your local machine.
```bash
git clone git@github.com:vitallcore/python-project-83.git
cd page-analyzer
```
Install dependencies using [Poetry](https://python-poetry.org/docs/).
```bash
make install
```
Create the new .env file and define SECRET_KEY and DATABASE_URL variables there. For example,
```bash
echo "SECRET_KEY=secret_key" >> .env
echo "DATABASE_URL=postgresql://user:password@host:port/database_name" >> .env
```
Initialize the database manualy or using provided bash script.
```bash
make build
```
Run the app.
```bash
# using Gunicorn
make start
# then open http://0.0.0.0:8000 in your browser


# or using the Flask development server with debug mode
make dev
# then open http://localhost:8000 in your browser
```
