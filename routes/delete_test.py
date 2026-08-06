from flask import url_for, flash, redirect

from routes import main_bp
from extensions import db
from models import Test


# Delete test route
@main_bp.route("/settings/delete/<int:test_id>", methods=["POST"])
def delete_test(test_id):
    t = Test.query.get_or_404(test_id)
    db.session.delete(t)
    db.session.commit()
    flash("Test deleted", "success")
    return redirect(url_for("main.settings"))
