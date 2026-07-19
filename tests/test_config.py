from app.core.config import Settings


def test_database_url_uses_host_and_port_by_default() -> None:
    settings = Settings(
        db_host="192.0.2.10",
        db_port=5433,
        db_name="petalops",
        db_user="postgres",
        db_password="secret",
    )

    assert settings.database_url.host == "192.0.2.10"
    assert settings.database_url.port == 5433
    assert settings.database_url.database == "petalops"
    assert settings.database_connection_target == "tcp:192.0.2.10:5433"


def test_database_url_uses_cloud_sql_socket_when_instance_is_configured() -> None:
    settings = Settings(
        db_host="136.119.27.100",
        db_port=5432,
        db_name="petalops",
        db_user="joindata",
        db_password="secret",
        db_cloud_sql_instance="flora-471805:us-central1:joindata",
    )

    assert settings.database_url.host is None
    assert settings.database_url.port is None
    assert settings.database_url.query["host"] == "/cloudsql/flora-471805:us-central1:joindata"
    assert settings.database_connection_target == "cloudsql:/cloudsql/flora-471805:us-central1:joindata"
