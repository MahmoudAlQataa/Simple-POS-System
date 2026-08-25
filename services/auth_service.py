from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "role" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "role" not in session:
            return redirect(url_for("main.login"))
        if session["role"] != "admin":
            flash("ما عندك صلاحية الوصول لهاي الصفحة", "error")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return wrapper