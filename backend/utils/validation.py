"""Validation helpers for request bodies and query params."""

from typing import Any


def validate_required_fields(payload: dict[str, Any], required_fields: list[str]) -> None:
    """Raise a ValueError when required fields are missing."""
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
