from flask import request, url_for, flash, redirect
from datetime import date, datetime

from routes import main_bp
from extensions import db
from models import Expense


# add route
@main_bp.route("/add", methods=['POST'])  # pulling the data from the front-end
def add():  # the data send by method='POST', action={{url_for('add')}}
    # pulling the data
    name = (request.form.get("name") or "").strip()  # this mean return somthing or an empety string but don't return null
    phone_str = (request.form.get("phone") or "").strip()  # this mean return somthing or an empety string but don't return null
    price_str = (request.form.get("price") or "").strip()
    paid_amount_str = (request.form.get("paid_amount") or "").strip()
    remain_amount_str = (request.form.get("remain_amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    # making sure that the user enter the full data
    if not name or not paid_amount_str or not price_str or not category:
        flash("please Fill the Missing Data", "error")  # the error massage
        return redirect(url_for("main.index"))

    # making sure the user entered a valid num (+num)
    try:
        paid_amount = float(paid_amount_str)
        if paid_amount <= 0:
            raise ValueError  # calling the error massage
    except ValueError:
        flash("Amount Must be a Positive Number", "error")
        return redirect(url_for("main.index"))

    # try to make the date in the right format
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d = date.today
    #
    try:
        price = float(price_str) if price_str else 0.0
        remain_amount = paid_amount - price
    except ValueError:
        flash("Invalid price value", "error")
        return redirect(url_for("main.index"))

    try:
        phone = int(phone_str) if price_str else 0000000000
    except ValueError:
        flash("Invalid phone value", "error")
        return redirect(url_for("main.index"))

    # adding the data into the database
    e = Expense(name=name, phone=phone, price=price, paid_amount=paid_amount, remain_amount=remain_amount, category=category, date=d)
    db.session.add(e)
    db.session.commit()

    flash("Expense added", "success")
    print(f" * Form Received : {dict(request.form)}")
    return redirect(url_for("main.index"))
