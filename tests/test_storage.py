from io import BytesIO

from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from app.services import storage


def test_construir_url_publica_s3_uses_public_base_url(monkeypatch) -> None:
    monkeypatch.setattr(storage.settings, "aws_s3_public_base_url", "https://cdn.example.com/media/")
    monkeypatch.setattr(storage.settings, "cloudfront_domain", "ignored.cloudfront.net")

    assert storage.construir_url_publica_s3("tenants/demo/foto.jpg") == (
        "https://cdn.example.com/media/tenants/demo/foto.jpg"
    )


def test_construir_url_publica_s3_uses_cloudfront(monkeypatch) -> None:
    monkeypatch.setattr(storage.settings, "aws_s3_public_base_url", None)
    monkeypatch.setattr(storage.settings, "cloudfront_domain", "https://cdn.example.com/")

    assert storage.construir_url_publica_s3("tenants/demo/foto.jpg") == (
        "https://cdn.example.com/tenants/demo/foto.jpg"
    )


def test_construir_url_publica_s3_uses_regional_s3_url(monkeypatch) -> None:
    monkeypatch.setattr(storage.settings, "aws_s3_public_base_url", None)
    monkeypatch.setattr(storage.settings, "cloudfront_domain", None)
    monkeypatch.setattr(storage.settings, "aws_s3_bucket", "petalops-assets")
    monkeypatch.setattr(storage.settings, "aws_region", "sa-east-1")

    assert storage.construir_url_publica_s3("tenants/demo/foto.jpg") == (
        "https://petalops-assets.s3.sa-east-1.amazonaws.com/tenants/demo/foto.jpg"
    )


def test_extension_imagen_rejects_unsupported_file_type() -> None:
    file = UploadFile(
        file=BytesIO(b"fake-image"),
        filename="perfil.gif",
        headers=Headers({"content-type": "image/gif"}),
    )

    try:
        storage._extension_imagen(file)
    except HTTPException as exc:
        assert exc.status_code == 415
    else:
        raise AssertionError("Expected unsupported image type")
