from flask import url_for, flash, redirect, request

from routes import main_bp
from extensions import db
from models import Expense
from services.receipt_service import delete_receipt
from services.auth_service import login_required

# Delete route
@main_bp.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete(expense_id):
    e = Expense.query.get_or_404(expense_id)  # Get the expense by ID or return 404 if not found

    delete_receipt(e)  # حذف ملف الوصل المرتبط قبل حذف السجل من القاعدة

    db.session.delete(e)  # Delete the expense from the database
    db.session.commit()  # Commit the changes to the database
    flash("Expense deleted", "success")  # Flash a success massage
    if request.referrer:
        return redirect(request.referrer)  # Redirect back to the previous page
    # return redirect(url_for("main.index"))  # Redirect back to the index page