from fastapi.testclient import TestClient

from app.core.config import settings


def test_healthcheck(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/healthcheck/")
    assert response.status_code == 200
