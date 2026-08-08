"""Application entry point for the GraphHire AI Flask service."""

from flask import Flask

from backend.config import Config
from backend.database import db
from backend.middleware.error_handlers import register_error_handlers
from backend.routes import register_blueprints

def create_app(config_class: type[Config] | None = None) -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    db.init_app(app)
    register_blueprints(app)
    register_error_handlers(app)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        return response

    @app.get("/")
    def health_check():
        return {"status": "ok", "service": "GraphHire AI"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(app.config["PORT"]))
