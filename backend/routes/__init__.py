"""Blueprint registration for the GraphHire AI backend."""

from routes.developer_routes import developer_bp

def register_blueprints(app) -> None:
    """Register all Flask blueprints with the application."""
    app.register_blueprint(developer_bp)
