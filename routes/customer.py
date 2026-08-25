from flask import render_template, request, flash
from services import parse_date_or_none, get_tests

from routes import main_bp
from models import Expense, Customer
from extensions import db
from datetime import date
from services.auth_service import admin_required

@main_bp.route("/customer/<int:customer_id>", methods=["GET"])
@admin_required
def customer_profile(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "").strip()
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)
    show_outstanding = request.args.get("show_outstanding") == "1"
    show_overpaid = request.args.get("show_overpaid") == "1"

    if start_date and end_date and end_date < start_date:
        flash("End date can't be earlier than start date", "error")
        start_date = end_date = None
        start_str = end_str = ""

    q = Expense.query.filter(Expense.customer_id == customer_id)

    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    if selected_category:
        q = q.filter(Expense.category.contains(selected_category))
    if show_outstanding and show_overpaid:
        q = q.filter(Expense.remain_amount != 0)
    elif show_outstanding:
        q = q.filter(Expense.remain_amount < 0)
    elif show_overpaid:
        q = q.filter(Expense.remain_amount > 0)

    expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()
    total = round(sum(e.price - e.discount for e in expenses), 2)
    total_paid = round(sum(e.paid_amount for e in expenses), 2)
    total_outstanding = round(sum(e.remain_amount for e in expenses if e.remain_amount < 0), 2)
    total_overpaid = round(sum(e.remain_amount for e in expenses if e.remain_amount > 0), 2)

    return render_template(
        "customer.html",
        customer=customer,
        expenses=expenses,
        total=total,
        total_paid=total_paid,
        total_outstanding=total_outstanding,
        total_overpaid=total_overpaid,
        categories=get_tests(),
        start_str=start_str,
        end_str=end_str,
        selected_category=selected_category,
        show_outstanding=show_outstanding,
        show_overpaid=show_overpaid,
    )