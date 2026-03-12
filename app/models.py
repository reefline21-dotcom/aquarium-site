import json
import os
import shutil
from typing import Any, Dict, List

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .config import get_config


def _safe_join(root: str, *parts: str) -> str:
    """
    Join one or more path components to a root, ensuring the final path
    stays inside the root (prevents ../ traversal).
    """
    joined = os.path.abspath(os.path.join(root, *parts))
    root_abs = os.path.abspath(root)
    if not os.path.commonpath([joined, root_abs]) == root_abs:
        raise ValueError("unsafe path")
    return joined


def _backup_file(path: str) -> None:
    """
    Rotate backups for the given file, keeping a limited number of versions.
    """
    cfg = get_config()
    if not os.path.exists(path):
        return

    base = f"{path}.bak"
    # Shift older backups up (file.bak.1 -> file.bak.2, ...)
    for idx in range(cfg.backup_versions - 1, 0, -1):
        src = f"{base}.{idx}"
        dst = f"{base}.{idx + 1}"
        if os.path.exists(src):
            os.replace(src, dst)
    # Current backup
    first = f"{base}.1"
    shutil.copy2(path, first)


def load_fish() -> Any:
    cfg = get_config()
    with open(cfg.data_file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_fish(data: Any) -> None:
    cfg = get_config()
    data_path = cfg.data_file_path

    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    _backup_file(data_path)

    tmp_path = f"{data_path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, data_path)


def upload_images(
    category: str, subcategory: str | None, files: List[FileStorage]
) -> List[str]:
    cfg = get_config()

    category = (category or "").strip()
    subcategory = (subcategory or "").strip()
    if not category:
        raise ValueError("category required")

    # Build safe target under img_root_path
    target_parts = [secure_filename(category)]
    if subcategory:
        target_parts.append(secure_filename(subcategory))

    target = _safe_join(cfg.img_root_path, *target_parts)
    os.makedirs(target, exist_ok=True)

    paths: List[str] = []
    for storage in files:
        filename = secure_filename(storage.filename or "")
        if not filename:
            continue
        _, ext = os.path.splitext(filename)
        if ext.lower() not in cfg.allowed_image_extensions:
            raise ValueError("unsupported file type")
        if storage.content_length is not None and storage.content_length > cfg.max_upload_bytes:
            raise ValueError("file too large")

        dest = os.path.join(target, filename)
        storage.save(dest)
        rel = os.path.relpath(dest, cfg.base_dir).replace("\\", "/")
        paths.append(rel)

    return paths


def delete_file(path: str) -> Dict[str, str]:
    if not path:
        raise ValueError("path required")

    cfg = get_config()
    full = _safe_join(cfg.base_dir, path)
    if os.path.exists(full) and os.path.isfile(full):
        os.remove(full)
        return {"status": "deleted"}

    raise FileNotFoundError("not found")


def delete_folder(path: str) -> Dict[str, str]:
    if not path:
        raise ValueError("path required")

    cfg = get_config()
    full = _safe_join(cfg.base_dir, path)
    if os.path.isdir(full):
        shutil.rmtree(full)
        return {"status": "deleted"}

    raise NotADirectoryError("not a directory")

