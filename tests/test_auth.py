from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_domiciliario_validates_payload() -> None:
    response = client.post("/api/v1/auth/domiciliarios/login", json={})

    assert response.status_code == 422


def test_perfil_domiciliario_requires_token() -> None:
    response = client.get("/api/v1/auth/domiciliarios/me")

    assert response.status_code == 401


def test_actualizar_foto_domiciliario_requires_token() -> None:
    response = client.patch(
        "/api/v1/auth/domiciliarios/me/foto",
        json={"foto_url": "https://example.com/foto.jpg"},
    )

    assert response.status_code == 401


def test_subir_foto_domiciliario_requires_token() -> None:
    response = client.post(
        "/api/v1/auth/domiciliarios/me/foto",
        files={"foto": ("perfil.jpg", b"fake-image", "image/jpeg")},
    )

    assert response.status_code == 401
