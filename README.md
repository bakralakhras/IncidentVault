# 🚨 IncidentVault Microservice

A production-grade microservice built with **FastAPI**, designed to manage incident reporting with full DevSecOps integration. It features database migrations, containerization, infrastructure-as-code, CI/CD readiness, observability, and testing—all in one clean, modular Python project.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-💨-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)
![Terraform](https://img.shields.io/badge/Terraform-Cloud--Ready-purple)
![Pytest](https://img.shields.io/badge/Tests-Pytest-yellow)
![Helm](https://img.shields.io/badge/Helm-Deployed-blueviolet)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-red)

---

## 🧰 Tech Stack

- **Backend Framework:** FastAPI (async, typed REST API)
- **ORM & DB:** SQLAlchemy + PostgreSQL + Alembic (versioned migrations)
- **Validation:** Pydantic
- **Testing:** Pytest (unit and integration tests with SQLite)
- **Monitoring:** Prometheus + FastAPI Instrumentator
- **Infrastructure:** Docker, Terraform, Kubernetes (Helm via Minikube)
- **CI/CD:** GitHub Actions (pre-commit hooks, tests, linting)
- **Cloud Ready:** Terraform configs built for future deployment to AWS or other cloud platforms

---

## 📁 Project Structure

```
.
├── alembic/                  # Alembic migrations (versioned schema)
├── db/                       # SQLAlchemy models and database session
├── routes/                   # Modular API routers (health, report)
├── tests/                    # Pytest test suite
├── terraform/                # Infrastructure as Code (IaC) for future cloud use
├── helm/                     # Helm charts for Kubernetes deployment (Minikube)
├── Dockerfile                # Multi-stage Docker image
├── requirements.txt
└── main.py                   # Application entrypoint
```

---

## 🚀 Getting Started

### 1. Clone & Setup Environment

```bash
git clone https://github.com/your-username/incidentvault.git
cd incidentvault
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root:

```env
DATABASE_URL=sqlite:///./incidentvault.db
```

---

## 🔃 Database Migrations with Alembic

To initialize and upgrade the schema:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "Add severity to reports"
```

---

## 🧪 Running Tests

Test your API and database integration:

```bash
pytest
```

Includes:
- Happy path tests for `/report`
- Validation error assertions
- Error handler verification
- SQLite test DB with teardown

---

## 🐳 Dockerized Deployment

Build and run locally:

```bash
docker build -t incidentvault .
docker run -d -p 8000:8000 incidentvault
```

---

## ☸️ Helm + Kubernetes (Deployed via Minikube)

This project is fully Kubernetes-ready and deployable with **Helm**. Deployment and testing were completed using **Minikube** locally.

To deploy:

```bash
helm install incidentvault ./helm
```

Or upgrade:

```bash
helm upgrade incidentvault ./helm
```

Included files:

- `helm/values.yaml` – Image config, ports, env variables
- `helm/templates/deployment.yaml`
- `helm/templates/service.yaml`
- `helm/templates/ingress.yaml` (optional)
- `helm/templates/configmap.yaml`
- `helm/templates/secrets.yaml`

---

## 🌍 Terraform Infrastructure (For Future Cloud Deployment)

The `terraform/` folder contains infrastructure-as-code setup prepared for eventual deployment to cloud platforms like AWS or GCP.

> ⚠️ This setup is **not yet deployed**, but fully prepared for future use with:
> - S3 remote state
> - IAM roles
> - EC2/RDS modules

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

---

## 📈 Observability

Prometheus-compatible metrics exposed at:

```
GET /metrics
```

---

## 🧹 Code Quality

Run linters & formatters:

```bash
black .
isort .
flake8
```

---

## 🤝 Contributing

1. Fork this repository
2. Create a new feature branch
3. Commit your changes and open a PR

---

## 📄 License

MIT License — 2025 © Your Name

---

## ⚙️ CI/CD with GitHub Actions

This project comes with a production-grade CI/CD workflow configured via **GitHub Actions**.

Located in `.github/workflows/cicd.yml`, it includes:

- 🔍 **Linting:** `flake8`, `black`, and `isort`
- 🧪 **Testing:** Runs full `pytest` test suite
- 🐳 **Docker Build:** Builds and optionally pushes Docker image
- ☁️ **Terraform Plan:** For infrastructure planning (optional future cloud use)

Workflow triggers:
- On every push to `main`
- On pull requests to run automated checks before merging

The goal: **automate, validate, and ship with confidence** 💪

