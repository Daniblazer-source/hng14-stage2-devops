# HNG12 Stage 2: Distributed Task Processing System

## 🚀 Project Overview
This project is a containerized microservices application. It uses a **FastAPI API** to receive jobs, **Redis** as a message broker, and a **Python Worker** to process tasks asynchronously.

## 📋 Prerequisites
Before starting, ensure your machine has the following installed:
* **Docker:** (v20.10+)
* **Docker Compose:** (v2.0+)
* **Git:** To clone the repository.
* **Ports Available:** Ensure ports `8000` (API) and `3000` (Frontend) are not being used by other services.

## 🚦 Getting Started (From Scratch)

### 1. Clone the Repository
```bash
git clone gitHub.com/Daniblazer-source/hng14-stage2-devops.git
cd hng14-stage2-devops
```


 ### 2. Environment Setup
The application requires environment variables to connect the services.

```Bash
cp .env.example .env
```


Bring Up the Stack
Run the following command to build the images and start the containers in detached mode:

```Bash
docker compose up --build -d
```

What a Successful Startup Looks Like
Once the command finishes, verify the deployment using these three checks:

Process Check: Run docker compose ps. You should see 4 services (api, worker, frontend, redis) with a status of Up or Healthy.

API Documentation: Navigate to `http://localhost:8000/docs`. You should see the FastAPI Swagger UI.

Automated Verification: Run the integration script to test the end-to-end flow:

```Bash
chmod +x integration.sh
./integration.sh
A successful run will output "Integration tests passed!"
```

### 3.🏗️ Architecture
API: Handles HTTP requests and job queuing.

Worker: Consumes jobs from Redis.

Redis: Acts as the database and message broker.

Frontend: User interface.

### 4.🛡️ DevOps Best Practices
Multi-stage Builds: Optimized for size and security.

Non-root Users: Services run as appuser.

Healthchecks: Containers self-report their readiness.
