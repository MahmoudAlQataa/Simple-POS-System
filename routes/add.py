from flask import request, url_for, flash, redirect
from datetime import date, datetime

from routes import main_bp
from extensions import db
from models import Expense, Test, Customer
from services.receipt_service import generate_receipt
from services.payment_service import apply_fifo_credit
from services.payment_receipt_service import generate_payment_receipt
from services.auth_service import login_required

# add route
@main_bp.route("/add", methods=['POST'])  # pulling the data from the front-end
@login_required
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

    # Customer linkage: use the selected customer_id if provided,
    # otherwise create a new Customer record automatically.
    customer_id_str = (request.form.get("customer_id") or "").strip()
    if customer_id_str:
        customer = Customer.query.get(int(customer_id_str))
        if customer is None:
            flash("Selected customer not found", "error")
            return redirect(url_for("main.index"))
        # keep the customer's phone in sync with the latest entered value
        if phone:
            customer.phone = phone
    else:
        customer = Customer(name=name, phone=phone, gender=gender)
        db.session.add(customer)
        db.session.flush()  # to get customer.id before creating the Expense

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
        customer_id=customer.id,
        )
    
    db.session.add(e)
    db.session.commit()

    generate_receipt(e)

    # if this customer has any leftover surplus from a previous payment, auto-apply it
    affected = apply_fifo_credit(customer.id)
    for invoice in affected:
        try:
            generate_receipt(invoice)
        except RuntimeError as err:
            flash(str(err), "error")

    if affected:
        try:
            generate_payment_receipt(customer, affected=affected)
        except RuntimeError as err:
            flash(str(err), "error")

    flash("Expense added", "success")
    print(f" * Form Received : {dict(request.form)}")
    return redirect(url_for("main.index"))
