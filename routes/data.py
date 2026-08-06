from flask import render_template, request, flash
from services import parse_date_or_none, get_tests

from routes import main_bp
from models import Expense


# data route - show all expenses (date + category + amount)
@main_bp.route("/data", methods=["GET"])
def data():
    # # ======================== THE FILTERs ========================
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
    total_paid = round(sum(e.paid_amount for e in expenses), 2)  # sum of total paid amount
    total_outstanding = round(sum(e.remain_amount for e in expenses if e.remain_amount < 0), 2)  # sum of total that you need from the customer
    total_overpaid = round(sum(e.remain_amount for e in expenses if e.remain_amount > 0), 2)  # sum of total thet the customer need from you
    return render_template(
        "data.html",
        expenses=expenses, 
        total=total, 
        total_paid=total_paid,
        total_outstanding=total_outstanding,
        total_overpaid=total_overpaid,
        categories=get_tests(),
        start_str=start_str,
        end_str=end_str,
        selected_category=selected_category,
        search_name=search_name,
        ) # sending the data to the front-end
