from functools import cached_property

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PetalOps Domicilios API"
    app_env: str = "local"
    app_debug: bool = False
    api_v1_prefix: str = "/api/v1"
    backend_cors_origins_raw: str = Field(
        default=(
            "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,"
            "http://localhost:5174,http://127.0.0.1:5174,"
            "https://domiapp.joindata.com.co"
        ),
        alias="BACKEND_CORS_ORIGINS",
    )

    db_host: str
    db_port: int = 5432
    db_name: str
    db_schema: str = "petalops"
    db_user: str
    db_password: str
    secret_key: str = "change-this-secret-in-production"
    access_token_expire_minutes: int = 480
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    aws_s3_bucket: str = Field(default="petalops-assets", alias="AWS_S3_BUCKET")
    aws_s3_public_base_url: str | None = Field(default=None, alias="AWS_S3_PUBLIC_BASE_URL")
    aws_s3_object_acl: str | None = Field(default=None, alias="AWS_S3_OBJECT_ACL")
    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    aws_session_token: str | None = Field(default=None, alias="AWS_SESSION_TOKEN")
    cloudfront_domain: str | None = Field(default=None, alias="CLOUDFRONT_DOMAIN")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @computed_field
    @cached_property
    def backend_cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins_raw.split(",")
            if origin.strip()
        ]

    @computed_field
    @cached_property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
