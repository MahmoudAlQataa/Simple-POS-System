from datetime import date
from flask import render_template, request

from routes import main_bp
from models import Bils
from services.date_service import parse_date_or_none
from services.auth_service import admin_required

@main_bp.route("/bils", methods=["GET"])
@admin_required
def bils():
    start_str = request.args.get("start", "")
    end_str = request.args.get("end", "")
    search_campany = request.args.get("search_campany", "").strip()

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    query = Bils.query

    if start_date:
        query = query.filter(Bils.bil_date >= start_date)
    if end_date:
        query = query.filter(Bils.bil_date <= end_date)
    if search_campany:
        query = query.filter(Bils.campany.ilike(f"%{search_campany}%"))

    bils = query.order_by(Bils.bil_date.desc(), Bils.bil_id.desc()).all()

    total = sum(b.bil_price for b in bils)
    total_paid = sum(b.bil_paid_amount for b in bils)
    total_outstanding = sum(b.bil_remain_amount for b in bils if b.bil_remain_amount < 0)
    total_overpaid = sum(b.bil_remain_amount for b in bils if b.bil_remain_amount > 0)

    return render_template(
        "bils.html",
        bils=bils,
        today=date.today().isoformat(),
        start_str=start_str,
        end_str=end_str,
        search_campany=search_campany,
        total=total,
        total_paid=total_paid,
        total_outstanding=total_outstanding,
        total_overpaid=total_overpaid,
        )