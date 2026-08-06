from flask import render_template

from routes import main_bp
from models import Test


# settings route - add a new test (name + price)
@main_bp.route("/settings", methods=["GET"])
def settings():
    tests = Test.query.order_by(Test.id.desc()).all()
    return render_template("settings.html", tests=tests)
