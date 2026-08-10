from fastapi.testclient import TestClient

from app.main import app
from app.services.auth import _es_domiciliario_externo, _normalizar_tipo_domiciliario


client = TestClient(app)


def test_login_domiciliario_validates_payload() -> None:
    response = client.post("/api/v1/auth/domiciliarios/login", json={})

    assert response.status_code == 422


def test_login_preflight_allows_local_vite_origin() -> None:
    response = client.options(
        "/api/v1/auth/domiciliarios/login",
        headers={
            "Origin": "http://127.0.0.1:5174",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5174"


def test_login_external_delivery_user_flag() -> None:
    assert _es_domiciliario_externo("Externo") is True
    assert _normalizar_tipo_domiciliario("Externo") == "externo"
    assert _es_domiciliario_externo("Interno") is False
    assert _normalizar_tipo_domiciliario("Interno") == "interno"


def test_perfil_domiciliario_requires_token() -> None:
    response = client.get("/api/v1/auth/domiciliarios/me")

    assert response.status_code == 401


def test_perfil_home_domiciliario_requires_token() -> None:
    response = client.get("/api/v1/auth/domiciliarios/me/perfil")

    assert response.status_code == 401


def test_desempeno_domiciliario_requires_token() -> None:
    response = client.get("/api/v1/auth/domiciliarios/me/desempeno")

    assert response.status_code == 401


def test_documentos_domiciliario_requires_token() -> None:
    response = client.get("/api/v1/auth/domiciliarios/me/documentos")

    assert response.status_code == 401


def test_vehiculo_domiciliario_requires_token() -> None:
    response = client.get("/api/v1/auth/domiciliarios/me/vehiculo")

    assert response.status_code == 401


def test_soporte_domiciliario_requires_token() -> None:
    response = client.get("/api/v1/auth/domiciliarios/me/soporte")

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
