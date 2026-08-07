"""Central error handling and HTTP exception mapping."""

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Register global error handlers for the Flask application."""

    @app.errorhandler(404)
    def not_found_error(_error):
        return jsonify({"error": "resource_not_found", "message": "The requested resource was not found."}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "internal_server_error", "message": "An unexpected error occurred."}), 500

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return jsonify({"error": error.name.lower().replace(" ", "_"), "message": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        return jsonify({"error": "unexpected_error", "message": str(error)}), 500
