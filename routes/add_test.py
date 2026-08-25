from flask import request, url_for, flash, redirect

from routes import main_bp
from extensions import db
from models import Test
from services.auth_service import admin_required

# add test route
@main_bp.route("/settings/add", methods=["POST"])
@admin_required
def add_test():
    name = (request.form.get("name") or "").strip()
    price_str = (request.form.get("price") or "").strip()

    if not name or not price_str:
        flash("please Fill the Missing Data", "error")
        return redirect(url_for("main.settings"))

    try:
        price = float(price_str)
        if price <= 0:
            raise ValueError
    except ValueError:
        flash("Price Must be a Positive Number", "error")
        return redirect(url_for("main.settings"))

    t = Test(name=name, price=price)
    db.session.add(t)
    db.session.commit()

    flash("Test added", "success")
    return redirect(url_for("main.settings"))