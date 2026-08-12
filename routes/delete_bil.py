from flask import redirect, url_for

from routes import main_bp
from models import Bils
from extensions import db


@main_bp.route("/bils/delete/<int:bil_id>", methods=["POST"])
def delete_bil(bil_id):
    bil = Bils.query.get_or_404(bil_id)

    db.session.delete(bil)
    db.session.commit()

    return redirect(url_for("main.bils"))