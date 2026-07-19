from pathlib import Path
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def _normalizar_cloudfront_domain(domain: str | None) -> str | None:
    if not domain:
        return None
    return domain.removeprefix("https://").removeprefix("http://").rstrip("/")


def _normalizar_base_url(url: str | None) -> str | None:
    if not url:
        return None
    return url.rstrip("/")


def _extension_imagen(file: UploadFile) -> str:
    if file.content_type in ALLOWED_IMAGE_TYPES:
        return ALLOWED_IMAGE_TYPES[file.content_type]

    suffix = Path(file.filename or "").suffix.lower()
    if suffix in ALLOWED_IMAGE_TYPES.values():
        return suffix

    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="La foto debe ser JPG, PNG o WEBP",
    )


def construir_url_publica_s3(s3_key: str) -> str:
    public_base_url = _normalizar_base_url(settings.aws_s3_public_base_url)
    if public_base_url:
        return f"{public_base_url}/{s3_key}"

    cloudfront_domain = _normalizar_cloudfront_domain(settings.cloudfront_domain)
    if cloudfront_domain:
        return f"https://{cloudfront_domain}/{s3_key}"

    if settings.aws_region == "us-east-1":
        return f"https://{settings.aws_s3_bucket}.s3.amazonaws.com/{s3_key}"

    return f"https://{settings.aws_s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"


def _s3_client():
    client_kwargs = {"region_name": settings.aws_region}
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        client_kwargs.update(
            {
                "aws_access_key_id": settings.aws_access_key_id,
                "aws_secret_access_key": settings.aws_secret_access_key,
            }
        )
        if settings.aws_session_token:
            client_kwargs["aws_session_token"] = settings.aws_session_token
    return boto3.client("s3", **client_kwargs)


def subir_foto_empleado(
    *,
    tenant_slug: str,
    id_empleado: int,
    file: UploadFile,
) -> tuple[str, str]:
    extension = _extension_imagen(file)
    s3_key = f"tenants/{tenant_slug}/empleados/{id_empleado}/perfil-{uuid4().hex}{extension}"

    try:
        file.file.seek(0)
        put_kwargs = {
            "Bucket": settings.aws_s3_bucket,
            "Key": s3_key,
            "Body": file.file.read(),
            "ContentType": file.content_type or "application/octet-stream",
        }
        if settings.aws_s3_object_acl:
            put_kwargs["ACL"] = settings.aws_s3_object_acl

        _s3_client().put_object(
            **put_kwargs,
        )
    except (NoCredentialsError, PartialCredentialsError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Credenciales AWS no configuradas para subir la foto a S3",
        ) from exc
    except (BotoCoreError, ClientError) as exc:
        error_code = None
        if isinstance(exc, ClientError):
            error_code = exc.response.get("Error", {}).get("Code")
        if not error_code:
            error_code = type(exc).__name__
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se pudo subir la foto a S3{f' ({error_code})' if error_code else ''}",
        ) from exc

    return s3_key, construir_url_publica_s3(s3_key)
