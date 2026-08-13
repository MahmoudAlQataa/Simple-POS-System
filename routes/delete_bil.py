from flask import redirect, url_for

from routes import main_bp
from models import Bils
from extensions import db
from services.receipt_service_bil import delete_bil_receipt


@main_bp.route("/bils/delete/<int:bil_id>", methods=["POST"])
def delete_bil(bil_id):
    bil = Bils.query.get_or_404(bil_id)

    delete_bil_receipt(bil)
    db.session.delete(bil)
    db.session.commit()

    return redirect(url_for("main.bils"))