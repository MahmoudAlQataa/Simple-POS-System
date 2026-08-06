from flask import render_template, request, flash
from datetime import date

from routes import main_bp
from models import Expense
from services import get_tests, parse_date_or_none


# the main route
@main_bp.route("/")
def index():
    # ======================== THE FILTERs ========================
    # read the start and end date from the front-end query parameters
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "").strip()
    # parse the start and end dates
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)
    search_name = (request.args.get("search_name") or "").strip()  # search by name
    #
    if start_date and end_date and end_date < start_date:
        flash("End date can't be earlier than start date", "error")
        start_date = end_date = None
        start_str = end_str = ""
    #
    q = Expense.query

    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)

    if selected_category:
        q = q.filter(Expense.category.contains(selected_category))

    if search_name:  # Name search (case-insensitive and partial)
        q = q.filter(Expense.name.ilike(f"%{search_name}%"))

    # pulling the data from the db
    expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()
    total = round(sum(e.price for e in expenses), 2)  # sum of price

    return render_template(
        "index.html",
        categories=get_tests(),
        today=date.today().isoformat(),
        expenses=expenses,
        total=total,
        start_str=start_str,
        end_str=end_str,
        selected_category=selected_category,
        search_name=search_name,
    )  # sending the data to the front-end