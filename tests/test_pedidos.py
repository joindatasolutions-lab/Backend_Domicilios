from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_pedidos_disponibles_requires_empresa_id() -> None:
    response = client.get("/api/v1/pedidos/disponibles")

    assert response.status_code == 422


def test_pedidos_disponibles_validates_date_format() -> None:
    response = client.get("/api/v1/pedidos/disponibles?empresa_id=3&fecha=no-es-fecha")

    assert response.status_code == 422


def test_asignarme_requires_token() -> None:
    response = client.post("/api/v1/pedidos/96650/asignarme")

    assert response.status_code == 401


def test_pedidos_asignados_requires_token() -> None:
    response = client.get("/api/v1/pedidos/asignados")

    assert response.status_code == 401


def test_devolver_requires_token() -> None:
    response = client.post("/api/v1/pedidos/96650/devolver")

    assert response.status_code == 401


def test_iniciar_entrega_requires_token() -> None:
    response = client.post("/api/v1/pedidos/96650/iniciar-entrega")

    assert response.status_code == 401


def test_entregar_requires_token() -> None:
    response = client.post("/api/v1/pedidos/96650/entregar", json={})

    assert response.status_code == 401


def test_no_entregado_requires_token() -> None:
    response = client.post("/api/v1/pedidos/96650/no-entregado", json={"motivo": "No responde"})

    assert response.status_code == 401


def test_novedad_requires_token() -> None:
    response = client.post(
        "/api/v1/pedidos/96650/novedad",
        json={"tipo_novedad": "cliente_no_disponible", "descripcion": "No responde"},
    )

    assert response.status_code == 401
