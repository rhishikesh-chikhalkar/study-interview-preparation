import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from flask import Flask

# Add src/ to sys.path for test resolution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from flask_rag_api import create_app
from flask_rag_api.config import TestingConfig


@pytest.fixture
def app() -> Flask:
    """Create and configure a new app instance for each test."""
    app_instance = create_app(TestingConfig)
    return app_instance


@pytest.fixture
def client(app: Flask) -> Generator:
    """A test client for the app."""
    with app.test_client() as client:
        yield client
