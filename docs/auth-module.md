# 1. User & Authentication Module 

This document details the implementation of the core User and Authentication features, including the structure of the service layer and the application of security best practices.

## 1.1. Service Layer Structure (`app/services/`)

The authentication logic is separated into two primary services to maintain the **Separation of Concerns** principle:

### A. `user_service.py` (Business Logic)

This service is responsible for all database interactions and core business logic related to the `User` entity.

| Method | Purpose | Key Logic |
| :--- | :--- | :--- |
| `create_user(db, user_data)` | Registers a new user. | 1. Checks for duplicate username or email (raising `UserAlreadyExistsError`), 2. Calls `security.hash_password()` before saving the user, 3. Persists the user model to the database |
### B. `security.py` (Cryptography & Tokens)

This service handles all cryptographic operations, ensuring that sensitive data is managed safely

| Method | Purpose | Security Detail |
| :--- | :--- | :--- |
| `hash_password(password)` | Hashes the plaintext password | Uses the Argon2 algorithm (via `passlib`) which is resistant to GPU attacks and considered modern best practice |
| `verify_password(...)` | Checks a plaintext password against a stored hash | Standard verification during login |
| `verify_and_update_password(...)` | Checks password and updates hash if outdated | Ensures security by upgrading old hash formats |
| `create_access_token(...)` | Generates a JWT (JSON Web Token) | **TODO:** This will be implemented when the login/token logic is added |

## 1.2. Router Implementation (`app/api/routers/auth_router.py`)

The `auth_router` handles all external API requests related to user accounts:

| Endpoint | Method | Pydantic Schema | Purpose | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `/auth/register` | `POST` | Input: `UserCreate`, Output: `UserResponse` | Registers a new user | `201` Success, `400` User Exists |
| `/auth/login` | `POST` | Input: `TokenRequest`, Output: `Token` | **TODO:** Logs in user and returns JWT | `200` Success, `401` Credentials Invalid |

* **Path Prefix:** All endpoints in this router are mounted under the **`/api/v1/`** prefix, as defined in `app/api/initial_routers.py`. This is why all unit tests must use the `/v1/` prefix (e.g: `/v1/health`).
* **Response Models:** Pydantic `response_model` ensures that the database model is stripped down to public-facing fields (`UserPublic`) before being returned, preventing accidental exposure of sensitive data like the hashed password.

## 1.2.1 Manual Verification (cURL Commands)
To quickly verify the functionaly of endpoints running, use the following curl commands from your host machine: 

### A. Successful Registration (Expected Status: 201 Created)
This registers a new unique user

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePassword123"
}'
```
### B. Failure: Duplicate Email (Expected Status: 400 Bad Request)
This test verifies that the `UserAlreadyExistsError` exception handler works correctly by
attempting to register the same user

```bash
# If used same username
{"status":"error","code":400,"message":"Username is already taken.","details":null}

# If used same email
{"status":"error","code":400,"message":"Email is already registered.","details":null}


```

---

## 1.3. Testing Strategy (`tests/test_main.py`)

* **Mocking:** Tests related to user creation (and future login) are structured to **mock** the database dependency (`app/core/database.py`). This ensures tests are fast and run without needing a real database connection.
* **CI Consistency:** The Pytest command is run inside the Docker container with explicit environment variables:
    ```bash
    docker compose exec backend sh -c 'PYTHONPATH=/app DATABASE_URL="sqlite:///:memory:" /usr/local/bin/python -m pytest /app/tests'
    ```
* **Path Resolution:** All test requests (e.g: `client.get("/v1/health")`) must include the `/v1` prefix to match the application's mounted router paths, avoiding the `404 Not Found` error.
