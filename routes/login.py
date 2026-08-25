from flask import render_template, request, session, redirect, url_for, flash
from routes import main_bp
import config


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == config.ADMIN_PASSWORD:
            session["role"] = "admin"
            return redirect(url_for("main.index"))
        elif password == config.WORKER_PASSWORD:
            session["role"] = "worker"
            return redirect(url_for("main.index"))
        else:
            flash("كلمة السر غير صحيحة", "error")
    return render_template("login.html")


@main_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("main.login"))