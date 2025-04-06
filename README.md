# InferAdmin

InferAdmin is a lightweight management web interface for local LLM infrastructure. It provides a simple API for deploying and managing docker-based inference engines.

## Features

- Deploy and monitor docker based inference engines
- Deploy and monitor docker based web interfaces
- Manage GPU and storage resources

## Installation

First git clone the repo, then use any of the following methods to install and run InferAdmin. Docker is the suggested way to run InferAdmin.

### Docker

1. Install Docker
2. Install Nvidia Container Toolkit
3. Run `docker compose up -d`

### Manual

1. Run `uv run inferadmin`