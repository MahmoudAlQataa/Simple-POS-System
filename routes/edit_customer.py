from flask import request, url_for, flash, redirect
from routes import main_bp
from extensions import db
from models import Customer, Expense
from services.auth_service import admin_required

@main_bp.route("/customer/<int:customer_id>/edit", methods=["POST"])
@admin_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    name = (request.form.get("name") or "").strip()
    phone_str = (request.form.get("phone") or "").strip()
    gender = (request.form.get("gender") or "").strip()

    if not name:
        flash("Name is required", "error")
        return redirect(url_for("main.customer_profile", customer_id=customer_id))

    if gender not in ("Male", "Female"):
        flash("Please select a valid gender", "error")
        return redirect(url_for("main.customer_profile", customer_id=customer_id))

    customer.name = name
    customer.phone = phone_str if phone_str else None
    customer.gender = gender

    # keep all linked Expense records in sync with the updated customer info
    Expense.query.filter_by(customer_id=customer.id).update({
        "name": name,
        "phone": customer.phone,
        "gender": gender,
    })

    db.session.commit()
    flash("Customer updated", "success")
    return redirect(url_for("main.customer_profile", customer_id=customer_id))