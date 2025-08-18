# Page Analyzer

## Project Description
Page Analyzer is a website that analyzes specified pages for SEO readiness, similar to PageSpeed Insights. 
It checks websites for key SEO elements and provides detailed reports.

## Hexlet tests and linter status:

[![Python CI](https://github.com/sroonla/python-project-83/actions/workflows/python-ci.yml/badge.svg)](https://github.com/sroonla/python-project-83/actions/workflows/python-ci.yml)
[![Hexlet tests and linter status](https://github.com/sroonla/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/sroonla/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sroonla_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=sroonla_python-project-83)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=sroonla_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=sroonla_python-project-83)
[![Render.com Demo](https://img.shields.io/badge/demo-Render.com-blue)](https://python-project-83-qwy4.onrender.com)

## Technologies Used

| Technology       | Description |
|------------------|-------------|
| UV | "An extremely fast Python package manager written in Rust. Designed as a replacement for pip and pip-tools." |
| Ruff | "Your Tool For Linter and Style Guide Enforcement" |
| Flask | "Lightweight WSGI web application framework for Python" |
| Gunicorn | "Production-grade WSGI HTTP Server for UNIX" |
| python-dotenv | "Reads key-value pairs from .env file and sets environment variables" |
| Bootstrap | "Frontend toolkit for responsive design" |
| Psycopg | "PostgreSQL database adapter for Python" |
| Validators | "Python Data Validation for Humans™" |
| Requests | "Elegant and simple HTTP library for Python" |
| Beautiful Soup | "Python library for pulling data out of HTML and XML files" |

## Installation

## Clone the repository:
git clone https://github.com/sroonla/python-project-83.git
cd python-project-83

## Configure environment variables:
cp .env_example .env

Edit .env and set SECRET_KEY and DATABASE_URL

## Install dependencies and initialize database:
make build

## Start the application:
make start

The application will be available at http://localhost:8000