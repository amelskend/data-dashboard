from app import database


def test_resolve_database_url_falls_back_to_sqlite_when_postgres_env_missing(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)

    assert database._resolve_database_url() == "sqlite:///./app.db"


def test_resolve_database_url_uses_explicit_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./override.db")

    assert database._resolve_database_url() == "sqlite:///./override.db"


def test_resolve_database_url_uses_postgres_env(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("POSTGRES_USER", "user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "password")
    monkeypatch.setenv("POSTGRES_DB", "dashboard")
    monkeypatch.setenv("POSTGRES_HOST", "db")
    monkeypatch.setenv("POSTGRES_PORT", "5433")

    database_url = database._resolve_database_url()
    assert database_url.startswith("postgresql://")
    assert "@db:5433/dashboard" in database_url
