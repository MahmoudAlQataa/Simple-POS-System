from flask import redirect, request, flash

from routes import main_bp
from models import Expense
from services.receipt_service import open_receipt


@main_bp.route("/receipt/<int:expense_id>/open", methods=["POST"])
def open_receipt_route(expense_id):
    e = Expense.query.get_or_404(expense_id)

    success = open_receipt(e)
    if not success:
        flash("Receipt file not found", "error")

    if request.referrer:
        return redirect(request.referrer)