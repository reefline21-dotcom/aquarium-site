import json
import os
from pathlib import Path

import pytest

from app import models
from app.config import Config
from app.services import FishService


def _make_temp_config(tmp_path: Path) -> Config:
    return Config(
        base_dir=str(tmp_path),
        data_dir="data",
        img_root="img",
        fish_file="fish.json",
        debug=False,
        admin_passcode="test",
        max_upload_bytes=1024 * 1024,
        allowed_image_extensions={".jpg"},
        backup_versions=2,
    )


def test_save_and_load_fish_roundtrip(tmp_path, monkeypatch):
    cfg = _make_temp_config(tmp_path)
    monkeypatch.setattr("app.models.get_config", lambda: cfg)

    data = [{"name": "Test Fish"}]
    models.save_fish(data)

    loaded = models.load_fish()
    assert loaded == data

    # backup should exist
    assert os.path.exists(cfg.data_file_path + ".bak.1")


def test_delete_file_and_folder_safe_paths(tmp_path, monkeypatch):
    cfg = _make_temp_config(tmp_path)
    monkeypatch.setattr("app.models.get_config", lambda: cfg)

    # file
    fpath = tmp_path / "foo.txt"
    fpath.write_text("x", encoding="utf-8")
    result = models.delete_file("foo.txt")
    assert result["status"] == "deleted"
    assert not fpath.exists()

    # folder
    dpath = tmp_path / "bar"
    dpath.mkdir()
    result = models.delete_folder("bar")
    assert result["status"] == "deleted"
    assert not dpath.exists()


def test_fish_service_validates_payload(monkeypatch, tmp_path):
    cfg = _make_temp_config(tmp_path)
    monkeypatch.setattr("app.models.get_config", lambda: cfg)

    svc = FishService()

    with pytest.raises(ValueError):
        svc.save_fish(None)

