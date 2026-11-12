"""Local hotel reception website; database credentials never leave the server."""
import os
import secrets
from flask import Flask, request, session, abort


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD"),
        MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config:
        app.config.update(test_config)

    @app.before_request
    def protect_forms():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        if request.method == "POST" and not secrets.compare_digest(
            session["csrf_token"].encode(), request.form.get("csrf_token", "").encode()
        ):
            abort(400, description="Phiên nhập liệu đã hết hạn. Hãy tải lại trang rồi thử lại.")

    @app.after_request
    def headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        return response

    from .routes import pages
    app.register_blueprint(pages)
    return app
