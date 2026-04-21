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