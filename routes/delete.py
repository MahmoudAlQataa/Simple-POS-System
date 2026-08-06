from flask import url_for, flash, redirect

from routes import main_bp
from extensions import db
from models import Expense


# Delete route
@main_bp.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    e = Expense.query.get_or_404(expense_id)  # Get the expense by ID or return 404 if not found
    db.session.delete(e)  # Delete the expense from the database
    db.session.commit()  # Commit the changes to the database
    flash("Expense deleted", "success")  # Flash a success massage
    return redirect(url_for("main.index"))  # Redirect back to the index page