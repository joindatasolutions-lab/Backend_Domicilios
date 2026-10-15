from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile
from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from app.api.v1.endpoints import pedidos
from app.core.security import CurrentDomiciliario, get_current_domiciliario
from app.db.session import get_db
from app.main import app
from app.services import storage


@pytest.fixture
def entrega(monkeypatch):
    captured = {"uploads": []}
    def guardar(db, **kwargs):
        captured.update(kwargs)
        return dict(status="ok", numero_pedido=123, id_pedido=1, id_entrega=2,
                    estado="entregado", domiciliario_id=7, mensaje="Entrega confirmada")
    def subir(**kwargs):
        captured["uploads"].append((kwargs["tipo"], kwargs["file"].file.read()))
        return "key", f'https://cdn.example.com/{kwargs["tipo"]}.png'
    monkeypatch.setattr(pedidos, "entregar_pedido", guardar)
    monkeypatch.setattr(pedidos, "subir_evidencia_entrega_pedido", subir)
    monkeypatch.setattr(pedidos, "_obtener_tenant_slug", lambda *args: "demo")
    app.dependency_overrides[get_db] = lambda: object()
    app.dependency_overrides[get_current_domiciliario] = lambda: CurrentDomiciliario(
        id_empleado=7, empresa_id=3, usuario="demo", cargo="domiciliario")
    try:
        with TestClient(app) as client:
            yield client, captured
    finally:
        app.dependency_overrides.clear()


def test_entrega_multipart_guarda_foto_y_firma(entrega):
    client, captured = entrega
    response = client.post("/api/v1/pedidos/123/entregar?sucursal_id=4",
        data={"firma_nombre": "Ana", "firma_documento": "123", "observaciones": "Recibido"},
        files={"foto": ("foto.png", b"foto", "image/png"),
               "firma": ("firma.png", b"firma", "image/png")})
    assert response.status_code == 200, response.text
    assert captured["uploads"] == [("foto", b"foto"), ("firma", b"firma")]
    assert captured["evidencia_foto_url"] == "https://cdn.example.com/foto.png"
    assert captured["firma_imagen_url"] == "https://cdn.example.com/firma.png"
    assert captured["firma_nombre"] == "Ana"
    assert captured["sucursal_id"] == 4


def test_entrega_json_compatible(entrega):
    client, captured = entrega
    response = client.post("/api/v1/pedidos/123/entregar", json={
        "evidencia_foto_url": "https://cdn.example.com/existente.jpg"})
    assert response.status_code == 200
    assert captured["evidencia_foto_url"] == "https://cdn.example.com/existente.jpg"
    assert captured["uploads"] == []


def test_valida_todos_los_archivos_antes_de_subir(entrega):
    client, captured = entrega
    response = client.post("/api/v1/pedidos/123/entregar", files={
        "foto": ("foto.png", b"foto", "image/png"),
        "firma": ("firma.gif", b"firma", "image/gif")})
    assert response.status_code == 415
    assert captured["uploads"] == []
    assert "numero_pedido" not in captured


def test_entrega_rechaza_json_invalido(entrega):
    client, captured = entrega
    response = client.post("/api/v1/pedidos/123/entregar", content="{",
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert "numero_pedido" not in captured


def test_entrega_no_confirma_si_falla_s3(entrega, monkeypatch):
    client, captured = entrega
    def fail(**kwargs):
        raise HTTPException(status_code=503, detail="No se pudo subir la foto a S3")
    monkeypatch.setattr(pedidos, "subir_evidencia_entrega_pedido", fail)
    response = client.post("/api/v1/pedidos/123/entregar",
                           files={"foto": ("foto.png", b"foto", "image/png")})
    assert response.status_code == 503
    assert "numero_pedido" not in captured


@pytest.mark.parametrize("tipo", ["foto", "firma"])
def test_storage_entrega_usa_ruta_por_empresa_y_pedido(monkeypatch, tipo):
    captured = {}
    class S3:
        def put_object(self, **kwargs):
            captured.update(kwargs)
    monkeypatch.setattr(storage, "_s3_client", lambda: S3())
    file = UploadFile(file=BytesIO(b"imagen"), filename="imagen.png",
                      headers=Headers({"content-type": "image/png"}))
    key, url = storage.subir_evidencia_entrega_pedido(
        tenant_slug="demo", numero_pedido=123, file=file, tipo=tipo)
    assert key.startswith(f"tenants/demo/domicilios/pedidos/123/entrega/{tipo}-")
    assert key.endswith(".png")
    assert captured["Body"] == b"imagen"
    assert captured["ContentType"] == "image/png"
    assert url.endswith(key)
