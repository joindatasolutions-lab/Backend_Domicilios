from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_database_health_returns_503_when_database_is_unavailable() -> None:
    class UnavailableDb:
        def execute(self, *args, **kwargs) -> None:
            raise SQLAlchemyError("connection timeout expired")

    def override_get_db():
        yield UnavailableDb()

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.get("/api/v1/health/db")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["detail"] == "No se pudo conectar con la base de datos"
