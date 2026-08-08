from flask import request, url_for, redirect, flash

from routes import main_bp
from extensions import db
from models import Expense
from services.receipt_service import generate_receipt


@main_bp.route("/edit/<int:id>", methods=["POST"])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    # Only editable fields
    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    paid_amount_str = (request.form.get("paid_amount") or "0").strip()
    discount_str = (request.form.get("discount") or "0").strip()

    try:
        paid_amount = float(paid_amount_str)
    except ValueError:
        paid_amount = 0.0

    try:
        discount = float(discount_str)
    except ValueError:
        discount = 0.0

    # Protection: The discount cannot exceed the original price.
    if discount > expense.price:
        discount = expense.price

    # The `price` is fixed and immutable, while `remain_amount` is always calculated server-side.
    expense.name = name
    expense.phone = phone
    expense.paid_amount = paid_amount
    expense.discount = discount
    expense.remain_amount = paid_amount - (expense.price - discount)  # Server account, not from the form

    db.session.commit()
    
    try:
        generate_receipt(expense)
    except RuntimeError as ex:
        flash(str(ex), "error")
    
    if request.referrer:
            return redirect(request.referrer)  # Redirect back to the previous page
    # return redirect(url_for("main.index"))
