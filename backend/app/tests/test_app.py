from app import __version__
from app.core.config import settings


def test_version():
    assert __version__ == "0.1.0"


def test_settings():
    assert settings.API_V1_STR == "/api/v1"
