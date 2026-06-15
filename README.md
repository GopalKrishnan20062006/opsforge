# OpsForge

OpsForge is a Python-based CLI tool designed to streamline the development, deployment, validation, monitoring, and release lifecycle of containerized services.

It provides a unified command-line interface for validating project structure, building Docker images, deploying services, monitoring health, generating release metadata, and managing service lifecycles.

---

# Project Overview

Modern applications require more than just source code. Developers must validate configurations, build artifacts, deploy services, monitor health, collect logs, and manage releases.

OpsForge simplifies these operational workflows through a single CLI interface.

Core capabilities include:

* Project validation
* Environment diagnostics
* Docker image builds
* Service deployment
* Health monitoring
* Service status inspection
* Log retrieval
* Release metadata generation
* Service destruction

---

# Architecture

The project follows a modular architecture.

```text
CLI Layer
    │
    ▼
Command Handlers
    │
    ├── Validator
    ├── Docker Operations
    ├── Health Monitoring
    ├── Release Management
    └── Diagnostics
    │
    ▼
Docker / FastAPI Service
```

Components:

* `cli.py` – User-facing commands
* `validator.py` – Configuration and file validation
* `docker_ops.py` – Docker operations
* `health.py` – Service health monitoring
* `release.py` – Release metadata generation
* `doctor.py` – Environment diagnostics
* `config.py` – YAML configuration loader

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd opsforge
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e .
```

Install development dependencies:

```bash
pip install pytest pytest-mock pytest-cov ruff pre-commit
```

---

# Commands

Validate project:

```bash
opsforge validate
```

Check environment:

```bash
opsforge doctor
```

Build Docker image:

```bash
opsforge build
```

Deploy service:

```bash
opsforge deploy
```

Check health:

```bash
opsforge health
```

View service status:

```bash
opsforge status
```

View logs:

```bash
opsforge logs
```

Generate release metadata:

```bash
opsforge release
```

Destroy deployed service:

```bash
opsforge destroy
```

---

# Example Workflow

```text
Source Code
     ↓
Validate
     ↓
Test
     ↓
Build
     ↓
Deploy
     ↓
Health
     ↓
Status / Logs
     ↓
Release
     ↓
Destroy
```

Typical workflow:

```bash
opsforge validate
pytest
opsforge build
opsforge deploy
opsforge health
opsforge status
opsforge logs
opsforge release
opsforge destroy
```

---

# Failure Scenarios

## Invalid Configuration

```bash
opsforge validate
```

Output:

```text
Validation failed
✗ Missing file: Dockerfile
```

## Failed Deployment

```bash
opsforge deploy
```

Output:

```text
✗ Deployment failed
```

## Health Check Failure

```bash
opsforge health
```

Output:

```text
✗ Service failed health check
```

## Docker Build Failure

```bash
opsforge build
```

Output:

```text
✗ Build failed
```

---

# Testing

The project includes automated unit and integration tests.

Test suites:

```text
test_validator.py
test_health.py
test_release.py
test_docker_ops.py
test_cli.py
```

Run all tests:

```bash
pytest -v
```

Run coverage:

```bash
pytest --cov=opsforge -v
```

Current coverage:

```text
61%+
```

---

# CI/CD

Quality checks include:

* Automated unit testing
* Mocked Docker failure testing
* Mocked Git metadata testing
* CLI integration testing
* Ruff linting
* Pre-commit hooks

Run linting:

```bash
ruff check .
```

Auto-fix formatting:

```bash
ruff check . --fix
```

---

# Project Structure

```text
opsforge/
│
├── opsforge/
│   ├── cli.py
│   ├── config.py
│   ├── doctor.py
│   ├── docker_ops.py
│   ├── health.py
│   ├── release.py
│   └── validator.py
│
├── tests/
│   ├── test_validator.py
│   ├── test_health.py
│   ├── test_release.py
│   ├── test_docker_ops.py
│   └── test_cli.py
│
├── Dockerfile
├── docker-compose.yml
├── opsforge.yaml
├── pyproject.toml
└── README.md
```

---

# Future Improvements

Planned enhancements:

* Automated release pipelines
* Container image registry integration
* Kubernetes deployment support
* Service metrics collection
* Prometheus integration
* Enhanced health monitoring
* Multi-environment deployments
* Structured logging support
* CI/CD pipeline templates
* Rollback support
* Notification integrations
* Deployment history tracking

---

# License

This project is intended for educational and learning purposes.
