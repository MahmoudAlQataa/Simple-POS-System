from datetime import date
from flask import render_template

from routes import main_bp
from models import Bils


@main_bp.route("/bils", methods=["GET"])
def bils():
    bils = Bils.query.order_by(Bils.bil_id.desc()).all()

    return render_template(
        "bils.html",
        bils=bils,
        today=date.today().isoformat(),
        )