from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Set


@dataclass(frozen=True)
class Config:
    """
    Central configuration for the aquarium site backend.

    Most values can be overridden via environment variables so they are not
    hard-coded into the codebase for production deployments.
    """

    # Core paths
    base_dir: str = field(
        default_factory=lambda: os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir)
        )
    )
    data_dir: str = "data"
    img_root: str = "img"
    fish_file: str = "fish.json"

    # Behavior flags
    debug: bool = field(
        default_factory=lambda: os.environ.get("FLASK_DEBUG", "0") == "1"
    )

    # Admin / auth
    admin_passcode: str = field(
        default_factory=lambda: os.environ.get("ADMIN_PASSCODE", "4616699")
    )

    # Upload constraints
    max_upload_bytes: int = 5 * 1024 * 1024  # 5MB per file
    allowed_image_extensions: Set[str] = field(
        default_factory=lambda: {".jpg", ".jpeg", ".png", ".webp"}
    )

    # Backup behavior
    backup_versions: int = 5

    @property
    def data_file_path(self) -> str:
        return os.path.join(self.base_dir, self.data_dir, self.fish_file)

    @property
    def img_root_path(self) -> str:
        return os.path.join(self.base_dir, self.img_root)


def get_config() -> Config:
    """
    Simple accessor so we can evolve to a more advanced config loading
    mechanism later without changing all call sites.
    """

    return Config()

