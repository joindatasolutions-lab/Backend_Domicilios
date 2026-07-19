from functools import cached_property

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


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
    backend_cors_origin_regex: str | None = Field(
        default=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
        alias="BACKEND_CORS_ORIGIN_REGEX",
    )

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str
    db_schema: str = "petalops"
    db_user: str
    db_password: str
    db_cloud_sql_instance: str | None = Field(default=None, alias="DB_CLOUD_SQL_INSTANCE")
    db_connect_timeout: int = Field(default=3, alias="DB_CONNECT_TIMEOUT")
    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=2, alias="DB_MAX_OVERFLOW")
    db_pool_recycle: int = Field(default=1800, alias="DB_POOL_RECYCLE")
    db_pool_timeout: int = Field(default=30, alias="DB_POOL_TIMEOUT")
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
    def database_url(self) -> URL:
        if self.db_cloud_sql_instance:
            return URL.create(
                "postgresql+psycopg",
                username=self.db_user,
                password=self.db_password,
                database=self.db_name,
                query={"host": f"/cloudsql/{self.db_cloud_sql_instance}"},
            )

        return URL.create(
            "postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @computed_field
    @cached_property
    def database_connection_target(self) -> str:
        if self.db_cloud_sql_instance:
            return f"cloudsql:/cloudsql/{self.db_cloud_sql_instance}"

        return f"tcp:{self.db_host}:{self.db_port}"


settings = Settings()
