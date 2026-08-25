from flask import flash, redirect, url_for
from routes import main_bp
from models import Customer
from services.payment_receipt_service import generate_payment_receipt, open_payment_receipt
from services.auth_service import admin_required

@main_bp.route("/customer/<int:customer_id>/statement/open", methods=["POST"])
@admin_required
def open_payment_receipt_route(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    opened = open_payment_receipt(customer)
    if not opened:
        # لو ما في ملف بعد (مثلاً زبون جديد بدون أي دفعة سابقة)، نولده أول مرة
        try:
            generate_payment_receipt(customer)
            open_payment_receipt(customer)
        except RuntimeError as e:
            flash(str(e), "error")

    return redirect(url_for("main.customer_profile", customer_id=customer_id))