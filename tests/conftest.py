"""Tests run in development mode: no Google sign-in, full access, and a fresh SQLite database per test."""

import os

import pytest

os.environ["NETPYQ_DEV_MODE"] = "1"


@pytest.fixture(autouse=True)
def fresh_database(tmp_path, monkeypatch):
    import pyq.config as config
    monkeypatch.setattr(config, "LOCAL_DB_FILE", tmp_path / "test.db")
