"""Helpers for converting Neo4j records into JSON-serializable data."""

from __future__ import annotations

from typing import Any

from neo4j.graph import Node, Path, Relationship


def serialize_value(value: Any) -> Any:
    """Convert Neo4j graph objects into plain Python structures."""
    if isinstance(value, Node):
        return {**value._properties}
    if isinstance(value, Relationship):
        return {"type": value.type, **value._properties}
    if isinstance(value, Path):
        return [serialize_value(node) for node in value.nodes]
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    if isinstance(value, tuple):
        return [serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serialize_value(item) for key, item in value.items()}
    return value


def serialize_record(record: Any) -> dict[str, Any]:
    """Serialize a Neo4j record into a dictionary."""
    return {key: serialize_value(value) for key, value in record.items()}
