from flask import redirect, request, flash

from routes import main_bp
from models import Bils
from services.receipt_service_bil import open_bil_receipt
from services.auth_service import admin_required

@main_bp.route("/bils/receipt/<int:bil_id>/open", methods=["POST"])
@admin_required
def open_bil_receipt_route(bil_id):
    bil = Bils.query.get_or_404(bil_id)

    success = open_bil_receipt(bil)
    if not success:
        flash("Receipt file not found", "error")

    if request.referrer:
        return redirect(request.referrer)