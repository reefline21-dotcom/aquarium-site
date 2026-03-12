from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Dict, Iterable, List, TypeVar, cast

from flask import jsonify, session
from werkzeug.datastructures import FileStorage

from . import models
from .config import get_config


T = TypeVar("T")


def api_handler(func: Callable[..., T]) -> Callable[..., Any]:
    """
    Decorator for API handlers that turns model-layer exceptions into
    consistent JSON responses.

    Using functools.wraps preserves the original function name so Flask
    endpoint names stay unique.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            return (
                jsonify({"error": {"message": str(exc), "code": "VALIDATION_ERROR"}}),
                400,
            )
        except FileNotFoundError as exc:
            return (
                jsonify({"error": {"message": str(exc), "code": "NOT_FOUND"}}),
                404,
            )
        except PermissionError as exc:
            return (
                jsonify({"error": {"message": str(exc), "code": "FORBIDDEN"}}),
                403,
            )
        except Exception as exc:  # pylint: disable=broad-except
            return (
                jsonify({"error": {"message": str(exc), "code": "SERVER_ERROR"}}),
                500,
            )

    return wrapper


@dataclass
class FishService:
    """
    High-level operations for working with fish data and media.

    This wraps the lower-level filesystem helpers in models.py so routes
    can call expressive methods and share error-handling via decorators.
    """

    def list_fish(self) -> Any:
        return models.load_fish()

    def save_fish(self, payload: Any) -> None:
        if payload is None:
            raise ValueError("no json")
        models.save_fish(payload)

    def upload_images(
        self,
        category: str,
        subcategory: str | None,
        files: Iterable[FileStorage],
    ) -> List[str]:
        files_list = list(files)
        return models.upload_images(
            category=category,
            subcategory=subcategory,
            files=cast(List[FileStorage], files_list),
        )

    def delete_file(self, path: str | None) -> Dict[str, str]:
        return models.delete_file(path or "")

    def delete_folder(self, path: str | None) -> Dict[str, str]:
        return models.delete_folder(path or "")


class AuthService:
    """
    Very small service responsible for admin auth concerns, including
    passcode verification and basic rate limiting on login attempts.
    """

    def __init__(self) -> None:
        self._cfg = get_config()

    def is_authenticated(self) -> bool:
        return bool(session.get("admin_authenticated"))

    def logout(self) -> None:
        session.pop("admin_authenticated", None)

    def can_attempt_login(self) -> bool:
        """
        Naive in-session rate limiting: after 5 failed attempts, block
        further attempts for the life of the session.
        """
        failures = int(session.get("admin_failures", 0))
        return failures < 5

    def record_failure(self) -> None:
        failures = int(session.get("admin_failures", 0)) + 1
        session["admin_failures"] = failures

    def reset_failures(self) -> None:
        session.pop("admin_failures", None)

    def try_login_with_passcode(self, code: str) -> bool:
        if not self.can_attempt_login():
            return False
        if code == self._cfg.admin_passcode:
            session["admin_authenticated"] = True
            self.reset_failures()
            return True
        self.record_failure()
        return False

