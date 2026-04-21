# Application Fixes - Stage 2 DevOps

This document logs all bugs, misconfigurations, and production gaps identified in the starter code, along with the corrective actions taken.

## 1. API Service (`api/main.py`)

### Hardcoded Redis Connection
- **Line**: 8
- **Issue**: The Redis client was initialized with `host="localhost"`. In a containerized environment, `localhost` refers to the API container itself rather than the Redis container, leading to a `ConnectionError`.
- **Fix**: Implemented `os.getenv()` to fetch `REDIS_HOST` and `REDIS_PORT` from environment variables, defaulting to `redis` and `6379` respectively.

### Missing CORS Middleware
- **Line**: N/A (Missing Entirely)
- **Issue**: The API lacked Cross-Origin Resource Sharing (CORS) configuration. Since the Frontend and API run on different ports/services, the browser's Same-Origin Policy would block all frontend requests to the API.
- **Fix**: Imported `CORSMiddleware` from `fastapi.middleware.cors` and configured the app to allow traffic from all origins (`*`) to ensure connectivity between services.

### Missing Dependency Imports
- **Line**: 1-5
- **Issue**: Standard libraries or middleware components used in the code (like `CORSMiddleware`) were not imported at the top of the file.
- **Fix**: Added the necessary import statements to prevent `NameError` during runtime.

---

## 2. Worker Service (`worker/main.py`)
### Hardcoded Redis Connection
- **Line**: 6
- **Issue**: Similar to the API, the worker was hardcoded to connect to `localhost`.
- **Fix**: Implemented `os.getenv()` to allow connection to the shared Redis service container.

### Lack of Error Handling / Graceful Shutdown
- **Line**: 14-19
- **Issue**: The worker loop did not handle connection interruptions or termination signals (SIGTERM). If Redis was temporarily unavailable, the worker would crash.
- **Fix**: Added a `try-except` block for `ConnectionError` and implemented a basic `signal` handler to ensure the worker shuts down cleanly when stopped by Docker.

---

## 3. Frontend Service (`frontend/app.js`)

### Hardcoded API Endpoint
- **Line**: 6
- **Issue**: The `API_URL` was hardcoded to `localhost:8000`. This prevents the frontend from communicating with the API when deployed in separate containers.
- **Fix**: Replaced the hardcoded string with `process.env.API_URL` to allow the API address to be injected at runtime via Docker Compose.


### Multi-stage Python Dependency Pathing
- **Issue**: Using `pip install --user` in the builder stage caused `ModuleNotFoundError` in the final stage because the Python pathing did not translate correctly between the root builder and the non-root runner.
- **Fix**: Implemented a Python Virtual Environment (`venv`) in the `/opt` directory to ensure all dependencies and executables are portable and correctly mapped in the final production image.



## 4. Infrastructure & CI/CD

### Docker Healthcheck Failures
- **Issue**: The API container lacked `curl`, and the Frontend lacked a root `/` route. This caused Docker to mark containers as `unhealthy`, preventing the stack from fully initializing.
- **Fix**: Switched the API healthcheck to a native Python socket check (removing the `curl` dependency) and added a basic `GET /` route to the Frontend.

### Docker Compose V2 Compatibility in CI
- **Issue**: The GitHub Actions runner failed when using the legacy `docker-compose` command (Exit 127).
- **Fix**: Updated the workflow to use the modern `docker compose` (V2) syntax supported by current Ubuntu runners.

### Security Vulnerabilities (Trivy)
- **Issue**: Docker images required automated scanning for "High" and "Critical" vulnerabilities as per production requirements.
- **Fix**: Integrated `aquasecurity/trivy-action` into the pipeline and ensured images were built locally within the scan job to allow for successful inspection.