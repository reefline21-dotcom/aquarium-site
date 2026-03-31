from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from app.services import AuthService


main_bp = Blueprint("main", __name__)
_auth = AuthService()


@main_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        code = (request.form.get("passcode") or "").strip()
        if not _auth.can_attempt_login():
            error = "Too many failed attempts. Please try again later."
        elif _auth.try_login_with_passcode(code):
            return redirect(url_for("main.admin_page"))
        else:
            error = "Invalid passcode. Please try again."
    return render_template("admin_login.html", error=error)


@main_bp.route("/admin/logout")
def admin_logout():
    _auth.logout()
    return redirect(url_for("main.admin_login"))


@main_bp.route("/admin")
def admin_page():
    # Require a simple passcode gate before loading the static admin UI
    if not _auth.is_authenticated():
        return redirect(url_for("main.admin_login"))
    return send_from_directory(current_app.static_folder, "admin.html")


@main_bp.route("/")
def root():
    return send_from_directory(current_app.static_folder, "index.html")

