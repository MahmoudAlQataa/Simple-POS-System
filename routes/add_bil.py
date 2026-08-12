from datetime import date
from flask import request, redirect, url_for, flash

from routes import main_bp
from models import Bils
from extensions import db


@main_bp.route("/bils/add", methods=["POST"])
def add_bil():
    bil_category = request.form.get("category", "").strip()
    campany = request.form.get("campany", "").strip()

    try:
        bil_price = float(request.form.get("price", ""))
    except (ValueError, TypeError):
        flash("Price is required and must be a number.")
        return redirect(url_for("main.bils"))

    try:
        bil_paid_amount = float(request.form.get("paid_amount", ""))
    except (ValueError, TypeError):
        bil_paid_amount = 0.0

    bil_date_str = request.form.get("date", "")
    try:
        bil_date = date.fromisoformat(bil_date_str)
    except (ValueError, TypeError):
        bil_date = date.today()

    if not bil_category or not campany:
        flash("Category and Campany are required.")
        return redirect(url_for("main.bils"))

    bil_remain_amount = bil_paid_amount - bil_price

    new_bil = Bils(
        bil_category=bil_category,
        campany=campany,
        bil_price=bil_price,
        bil_paid_amount=bil_paid_amount,
        bil_remain_amount=bil_remain_amount,
        bil_date=bil_date,
    )

    db.session.add(new_bil)
    db.session.commit()

    return redirect(url_for("main.bils"))