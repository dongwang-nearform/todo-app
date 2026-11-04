import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://todo:todo@127.0.0.1:5432/todo")

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db import engine
from app.main import app

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def migrate() -> None:
    cfg = Config(str(ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(ROOT / "alembic"))
    command.upgrade(cfg, "head")


@pytest.fixture(autouse=True)
def clean(migrate: None) -> None:
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE todos, lists, copies RESTART IDENTITY CASCADE"))


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def detail():
    def _detail(response) -> str:
        body = response.json()
        assert isinstance(body["detail"], str) and body["detail"]
        return body["detail"]

    return _detail


@pytest.fixture
def make_list(client: TestClient):
    def _make(name: str = "Saturday") -> dict:
        response = client.post("/api/lists", json={"name": name})
        assert response.status_code == 201, response.text
        return response.json()

    return _make


@pytest.fixture
def make_todo(client: TestClient):
    def _make(list_id: int, **fields) -> dict:
        body = {"title": "English drop-off", "priority": 3}
        body.update(fields)
        response = client.post(f"/api/lists/{list_id}/todos", json=body)
        assert response.status_code == 201, response.text
        return response.json()

    return _make
