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
*(Pending investigation—likely contains similar Redis connection issues)*

---

## 3. Frontend Service
*(Pending investigation)*