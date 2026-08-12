from flask import request, redirect, url_for, flash

from routes import main_bp
from models import Bils
from extensions import db


@main_bp.route("/bils/edit/<int:bil_id>", methods=["POST"])
def edit_bil(bil_id):
    bil = Bils.query.get_or_404(bil_id)

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

    if not bil_category or not campany:
        flash("Category and Campany are required.")
        return redirect(url_for("main.bils"))

    bil.bil_category = bil_category
    bil.campany = campany
    bil.bil_price = bil_price
    bil.bil_paid_amount = bil_paid_amount
    bil.bil_remain_amount = bil_paid_amount - bil_price  # Always calculated server-side

    db.session.commit()

    return redirect(url_for("main.bils"))