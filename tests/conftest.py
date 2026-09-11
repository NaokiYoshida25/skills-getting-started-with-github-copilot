import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Store initial deep copy of activities state
INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict to its initial state before each test."""
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    """Fixture that provides a FastAPI TestClient instance."""
    return TestClient(app)
