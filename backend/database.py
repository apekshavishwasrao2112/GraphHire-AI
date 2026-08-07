"""Database layer for the Neo4j-compatible Cognodb connection."""

import logging
from typing import Any

from flask import current_app
from neo4j import GraphDatabase, exceptions

logger = logging.getLogger(__name__)


class Database:
    """Wrapper around the Neo4j driver with connection pooling and error handling."""

    def __init__(self) -> None:
        self._driver = None

    def init_app(self, app) -> None:
        """Initialize the driver from Flask configuration."""
        self._driver = GraphDatabase.driver(
            app.config["COGNODB_URI"],
            auth=(app.config["COGNODB_USERNAME"], app.config["COGNODB_PASSWORD"]),
            max_connection_lifetime=3600,
            max_connection_pool_size=int(app.config.get("MAX_CONNECTIONS", 10)),
            connection_acquisition_timeout=int(app.config.get("REQUEST_TIMEOUT", 30)),
        )

    def get_driver(self):
        """Return the active driver instance."""
        return self._driver

    def ping(self) -> bool:
        """Check whether the database is reachable."""
        if self._driver is None:
            return False
        try:
            with self._driver.session() as session:
                session.run("RETURN 1")
            return True
        except exceptions.ServiceUnavailable:
            logger.exception("Database unavailable")
            return False
        except exceptions.ClientError as exc:
            logger.exception("Database client error: %s", exc)
            return False

    def run_query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Execute a parameterized Cypher query and return a list of records."""
        if self._driver is None:
            raise RuntimeError("Database driver has not been initialized")

        with self._driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]


# Shared database instance

db = Database()
