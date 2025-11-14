"""
Mock tests for CI verification
These tests mock the database to avoid requiring a real database connection
"""
import sys
from unittest.mock import MagicMock

# Mock the entire database module BEFORE any imports
mock_database = MagicMock()
mock_engine = MagicMock()
mock_session_local = MagicMock()

mock_database.engine = mock_engine
mock_database.SessionLocal = mock_session_local
mock_database.get_db = MagicMock()

# Inject mock into sys.modules BEFORE importing app
sys.modules['app.database'] = mock_database

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session

client = TestClient(app)


def test_simple_math():
    """Basic test that always passes"""
    assert 1 + 1 == 2
    assert "hello".upper() == "HELLO"


def test_imports_work():
    """Verify we can import our modules"""
    from app.main import app
    assert app is not None


def test_fastapi_app_exists():
    """Verify FastAPI app is created"""
    assert client is not None


def test_read_root():
    """Test the root endpoint returns correct message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Project Management API is running!"}


def test_health_check_success():
    """Test health endpoint when database connection succeeds"""
    # Mock the database session for this specific test
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}

    # Verify database was queried
    mock_db.execute.assert_called_once()

    app.dependency_overrides.clear()


def test_health_check_failure():
    """Test health endpoint when database connection fails"""
    # Mock database to raise an exception
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("Database connection error")
    app.dependency_overrides[get_session] = lambda: mock_db

    response = client.get("/health")

    assert response.status_code == 500
    assert response.json()["detail"] == "Database connection failed"

    app.dependency_overrides.clear()


def test_status_endpoint_success():
    """Test status endpoint when database connection succeeds"""
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db

    response = client.get("/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}

    app.dependency_overrides.clear()


def test_status_endpoint_failure():
    """Test status endpoint when database connection fails"""
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("Database error")
    app.dependency_overrides[get_session] = lambda: mock_db

    response = client.get("/status")

    assert response.status_code == 500
    assert response.json()["detail"] == "Database connection failed"

    # Cleanup
    app.dependency_overrides.clear()
