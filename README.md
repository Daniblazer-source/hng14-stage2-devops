# HNG12 Stage 2: Distributed Task Processing System

## 🚀 Project Overview
This project is a high-performance, containerized microservices application designed for asynchronous task processing. It demonstrates advanced DevOps practices including service orchestration, multi-stage Docker builds, and a robust CI/CD pipeline.

## 🏗️ Architecture
The system is composed of four primary components:
- **Frontend:** A React/Node.js interface for user interaction.
- **API (Backend):** A FastAPI service that validates requests and manages the job queue.
- **Worker:** A Python-based background processor that executes heavy computational tasks.
- **Redis:** A message broker and key-value store used for inter-service communication and state management.



## 🛠️ Key DevOps Features
- **Multi-Stage Builds:** Dockerfiles are optimized using the builder pattern to reduce image size and minimize the attack surface.
- **Non-Root Execution:** All services run as a dedicated `appuser` to implement the Principle of Least Privilege.
- **Service Discovery:** Services communicate via a named Docker network using internal DNS resolution.
- **Automated CI/CD:** A GitHub Actions workflow that performs:
  - **Linting:** (Flake8, ESLint, Hadolint)
  - **Security Scanning:** (Trivy)
  - **Integration Testing:** Automated verification of the full stack via Docker Compose.

## 🚦 Getting Started (Manual Clone)
1. **Clone & Environment:**
   ```bash
   git clone <repo-url>
   cp .env.example .env


   Spin up the stack:

Bash
docker compose up --build -d
Verify:

Bash
./integration.sh
🛡️ Security Implementation
Container Hardening: Used python-slim base images and removed build-time dependencies.

Pipeline Security: Trivy scans fail the build if any "CRITICAL" vulnerabilities are detected in the container layers.

Healthchecks: Implemented native Docker healthchecks to ensure service availability before traffic routing.

📊 CI/CD Status
Current Grading Score: 76/100

Status: Passed to Stage 3
