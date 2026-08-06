from flask import render_template
from datetime import date

from routes import main_bp
from models import Expense
from services import get_tests


# the main route
@main_bp.route("/")
def index():
    
    q = Expense.query
    expenses_today = q.filter(Expense.date == date.today()).order_by(Expense.date.desc(), Expense.id.desc()).all()
    total = round(sum(e.price-e.discount for e in expenses_today), 2)  # sum of price
    total_paid = round(sum(e.paid_amount for e in expenses_today), 2)  # sum of price
    total_outstanding = round(sum(e.remain_amount for e in expenses_today if e.remain_amount < 0), 2)  # sum of total that you need from the customer
    total_overpaid = round(sum(e.remain_amount for e in expenses_today if e.remain_amount > 0), 2)  # sum of total thet the customer need from you
    
    return render_template(
        "index.html",
        categories=get_tests(),
        today=date.today().isoformat(),
        expenses_today=expenses_today,
        total=total,
        total_paid=total_paid,
        total_outstanding=total_outstanding,
        total_overpaid=total_overpaid,
    )  # sending the data to the front-end