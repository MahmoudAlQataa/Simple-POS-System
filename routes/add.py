from flask import request, url_for, flash, redirect
from datetime import date, datetime

from routes import main_bp
from extensions import db
from models import Expense, Test
from services.receipt_service import generate_receipt


# add route
@main_bp.route("/add", methods=['POST'])  # pulling the data from the front-end
def add():  # the data send by method='POST', action={{url_for('add')}}
    # pulling the data
    name = (request.form.get("name") or "").strip()  # this mean return somthing or an empety string but don't return null
    phone_str = (request.form.get("phone") or "").strip()  # this mean return somthing or an empety string but don't return null
    price_str = (request.form.get("price") or "").strip()
    discount_str = (request.form.get("discount") or "").strip()
    paid_amount_str = (request.form.get("paid_amount") or "").strip()
    remain_amount_str = (request.form.get("remain_amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()
    gender = (request.form.get("gender") or "").strip()
    doctor_name = (request.form.get("doctor_name") or "").strip() or None

    # making sure that the user enter the full data
    if not name or not category:
        flash("please Fill the Missing Data", "error")  # the error massage
        return redirect(url_for("main.index"))

    # making sure the user entered a valid num (+num)
    try:
        paid_amount = float(paid_amount_str) if paid_amount_str else 0.0
        if paid_amount < 0:
            raise ValueError  # calling the error massage
    except ValueError:
        flash("Amount Must be Zero or Positive", "error")
        return redirect(url_for("main.index"))

    # try to make the date in the right format
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d = date.today()
    #
    # Recalculate the price server-side based on the actual analysis names (category)
    # Never trust the price_str value sent from the form
    test_names = [t.strip() for t in category.split(",") if t.strip()]
    all_tests = {t.name: t.price for t in Test.query.all()}

    price = 0.0
    for tn in test_names:
        if tn not in all_tests:
            flash(f"Unknown test: {tn}", "error")
            return redirect(url_for("main.index"))
        price += all_tests[tn]

    try:
        discount = float(discount_str) if discount_str else 0.0
    except ValueError:
        flash("Invalid discount value", "error")
        return redirect(url_for("main.index"))

    # The discount must not exceed the price actually calculated by the server.
    if discount > price:
        discount = price
    if discount < 0:
        discount = 0.0

    remain_amount = paid_amount - (price - discount)
    phone = phone_str if phone_str else None
    
    # Validation: Check the value against the allowed options (protection against tampering)
    if gender not in ("Male", "Female"):
        flash("Please select a valid gender", "error")
        return redirect(url_for("main.index"))

    # adding the data into the database
    e = Expense(
        name=name, 
        phone=phone, 
        price=price, 
        discount=discount, 
        paid_amount=paid_amount, 
        remain_amount=remain_amount, 
        category=category, 
        date=d,
        gender=gender,
        doctor_name=doctor_name,
        )
    
    db.session.add(e)
    db.session.commit()

    generate_receipt(e)

    flash("Expense added", "success")
    print(f" * Form Received : {dict(request.form)}")
    return redirect(url_for("main.index"))
