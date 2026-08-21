from flask import request, url_for, flash, redirect
from datetime import date

from routes import main_bp
from extensions import db
from models import Expense, Customer
from services.receipt_service import generate_receipt
from services.payment_service import apply_fifo_credit, PAYMENT_CATEGORY
from services.payment_receipt_service import generate_payment_receipt


@main_bp.route("/customer/<int:customer_id>/payment", methods=["POST"])
def customer_payment(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    amount_str = (request.form.get("amount") or "").strip()

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Please enter a valid payment amount", "error")
        return redirect(url_for("main.customer_profile", customer_id=customer_id))

    # create the payment record holding the full amount as surplus;
    # apply_fifo_credit() will distribute it across outstanding invoices
    payment = Expense(
        name=customer.name,
        phone=customer.phone,
        price=0.0,
        discount=0.0,
        paid_amount=amount,
        remain_amount=amount,
        category=PAYMENT_CATEGORY,
        date=date.today(),
        gender=customer.gender,
        doctor_name=None,
        customer_id=customer.id,
    )
    db.session.add(payment)
    db.session.commit()

    affected = apply_fifo_credit(customer.id)
    for invoice in affected:
        try:
            generate_receipt(invoice)
        except RuntimeError as e:
            flash(str(e), "error")

    try:
        generate_payment_receipt(customer, affected=affected)
    except RuntimeError as e:
        flash(str(e), "error")

    flash(f"Payment of {amount:.2f} recorded and distributed", "success")
    return redirect(url_for("main.customer_profile", customer_id=customer_id))