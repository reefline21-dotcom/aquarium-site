import os

from flask import Flask, jsonify, render_template, request

from .routes.api import api_bp
from .routes.main import main_bp


def create_app() -> Flask:
    """
    Application factory that wires together blueprints, configuration,
    static serving and error handlers.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    templates_dir = os.path.join(base_dir, "templates")

    app = Flask(
        __name__,
        static_folder=base_dir,  # serve static files from project root
        static_url_path="",
        template_folder=templates_dir,
    )
    # Simple session key; override with FLASK_SECRET_KEY in production
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(main_bp)

    # Error handlers
    @app.errorhandler(404)
    def handle_404(error):
        # JSON for API routes, HTML page for normal browser routes
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource not found"}), 404
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def handle_500(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error"}), 500
        return render_template("500.html"), 500

    return app

