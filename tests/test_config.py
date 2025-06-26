import importlib
import os
from unittest.mock import patch
from _pytest.monkeypatch import MonkeyPatch

from app.core import config


def test_settings_default_values() -> None:
    """
    Test that the settings object has the correct default values
    when no environment variables are set.
    """
    # Mock environment variables to provide required fields
    with patch.dict(os.environ, {
        'DATABASE_URL': 'dummy_db_url_for_validation',
        'JWT_SECRET_KEY': 'dummy_jwt_secret_for_validation'
    }, clear=True):
        # Create a fresh instance of settings
        settings = config.Settings(
            DATABASE_URL='dummy_db_url_for_validation',
            JWT_SECRET_KEY='dummy_jwt_secret_for_validation'
        )

        assert settings.PROJECT_NAME == "Adventure Guild API"
        assert settings.API_V1_STR == "/api/v1"
        assert settings.JWT_ALGORITHM == "HS256"
        # Update to match the actual default values from config.py
        assert settings.BACKEND_CORS_ORIGINS == [
            "https://adv-guild.com",
            "https://www.adv-guild.com",
            "http://localhost:3000",
            "http://localhost:8080",
        ]


def test_settings_loading_from_env(monkeypatch: MonkeyPatch) -> None:
    """
    Test that settings are correctly loaded from environment variables.
    """
    # Use monkeypatch to set environment variables for this test
    monkeypatch.setenv("PROJECT_NAME", "My Awesome Test Project")
    monkeypatch.setenv("API_V1_STR", "/api/v2/test")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", '["https://test.com"]')
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@db/test_db")

    # The `config` module is already imported, so the `settings` object was
    # already created. We must reload the module to force pydantic-settings
    # to re-read the environment variables we just set.
    importlib.reload(config)

    # The global `settings` object in the reloaded module should have the new values
    assert config.settings.PROJECT_NAME == "My Awesome Test Project"
    assert config.settings.API_V1_STR == "/api/v2/test"
    assert config.settings.BACKEND_CORS_ORIGINS == ["https://test.com"]
    assert config.settings.DATABASE_URL == "postgresql://test:test@db/test_db"
    assert config.settings.JWT_SECRET_KEY == "test-secret"