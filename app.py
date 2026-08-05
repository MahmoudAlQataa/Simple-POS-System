from flask import Flask, render_template, request, url_for, make_response, flash, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import socket

# intialaising the flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mahmoud-test-key' # a decode key for the cash data that stored in the setion

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db' # tell SQLAlchemy where the db is located 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # stop the tracking we don't need it yet
db = SQLAlchemy(app) # (Initialize SQLAlchemy) creat the db and connect it to the app

# Define the Expense table (model).
class Expense(db.Model): 
    #__tablename__ = "Expense" # if you want to spicefai the tabel name 
    # intialising the columns 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, nullable=False)
    remain_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    
# Define the Test table (model).
class Test(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
with app.app_context(): # Enter the Flask application context. (# go in the env)
    db.create_all() # Create all tables defined by the models (if they don't already exist).

# we need to make it entered by the user
def get_tests():
    tests = Test.query.order_by(Test.id.desc()).all()
    return tests
    # return [t.name for t in tests] # just the name 
    # return CATEGORIES

def parse_date_or_none(s: str):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


# the main route 
@app.route("/")
def index():
    # ======================== THE FILTERs ======================== 
    # read the start and end date from the front-end query parameters
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "" ).strip()
    # parse the start and end dates
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)
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
        q = q.filter(Expense.category == selected_category)
        
    # pulling the data from the db
    expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all() 
    total = round(sum(e.price for e in expenses), 2) # sum of price
    
    return render_template(
        "index.html",
        categories=get_tests(),
        today=date.today().isoformat(),
        expenses=expenses,
        total=total,
        start_str=start_str,
        end_str=end_str,
        selected_category=selected_category,
        ) # sending the data to the front-end


# add route
@app.route("/add", methods=['POST']) # pulling the data from the front-end 
def add(): # the data send by method='POST', action={{url_for('add')}} 
    # pulling the data
    name = (request.form.get("name") or "").strip() # this mean return somthing or an empety string but don't return null
    phone_str = (request.form.get("phone") or "").strip() # this mean return somthing or an empety string but don't return null
    price_str = (request.form.get("price") or "").strip()
    paid_amount_str = (request.form.get("paid_amount") or "").strip()
    remain_amount_str = (request.form.get("remain_amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    # making sure that the user enter the full data
    if not name or not paid_amount_str or not price_str or not category:
        flash("please Fill the Missing Data", "error") # the error massage
        return redirect(url_for("index"))
    
    # making sure the user entered a valid num (+num)
    try:
        paid_amount = float(paid_amount_str)
        if paid_amount <= 0:
            raise ValueError # calling the error massage
    except ValueError:
        flash("Amount Must be a Positive Number", "error")
        return redirect(url_for("index"))

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
        return redirect(url_for("index"))
    
    # try:
    #     phone = int(phone_str) if price_str else 0
    # except ValueError:
    #     flash("Invalid phone value", "error")
    #     return redirect(url_for("index"))
    
    # adding the data into the database
    e = Expense(name=name, phone=phone_str, price=price, paid_amount=paid_amount, remain_amount=remain_amount, category=category, date=d)
    db.session.add(e)
    db.session.commit()

    flash("Expense added", "success")
    print(f" * Form Received : {dict(request.form)}")
    return redirect(url_for("index"))

# Delete route
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    e = Expense.query.get_or_404(expense_id) # Get the expense by ID or return 404 if not found
    db.session.delete(e) # Delete the expense from the database
    db.session.commit() # Commit the changes to the database
    flash("Expense deleted", "success") # Flash a success massage
    return redirect(url_for("index")) # Redirect back to the index page

# settings route - add a new test (name + price)
@app.route("/settings", methods=["GET"])
def settings():
    tests = Test.query.order_by(Test.id.desc()).all()
    return render_template("settings.html", tests=tests)

# add test route
@app.route("/settings/add", methods=["POST"])
def add_test():
    name = (request.form.get("name") or "").strip()
    price_str = (request.form.get("price") or "").strip()

    if not name or not price_str:
        flash("please Fill the Missing Data", "error")
        return redirect(url_for("settings"))

    try:
        price = float(price_str)
        if price <= 0:
            raise ValueError
    except ValueError:
        flash("Price Must be a Positive Number", "error")
        return redirect(url_for("settings"))

    t = Test(name=name, price=price)
    db.session.add(t)
    db.session.commit()

    flash("Test added", "success")
    return redirect(url_for("settings"))

# Delete test route
@app.route("/settings/delete/<int:test_id>", methods=["POST"])
def delete_test(test_id):
    t = Test.query.get_or_404(test_id)
    db.session.delete(t)
    db.session.commit()
    flash("Test deleted", "success")
    return redirect(url_for("settings"))

# export route
@app.route("/export.csv")
def export_csv():
    # read the start and end date from the front-end query parameters
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "" ).strip()
    # parse the start and end dates
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    q = Expense.query
    
    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    
    if selected_category:
        q = q.filter(Expense.category == selected_category)
        
    expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all() # pulling the data from the db
    lines = ["date, name, phone, category, price, paid_amount, remain_amount"] # header line

    for e in expenses:
        lines.append(f"{e.date.isoformat()}, {e.name}, {e.phone}, {e.category}, {e.price:.2f}, {e.paid_amount:.2f}, {e.remain_amount:.2f}")
    csv_data = "\n".join(lines)

    fname_start = start_str or "all"
    fname_end = end_str or "all"
    filename = f"expenses_{fname_start}_to_{fname_end}.csv"
    
    return Response(
        csv_data,
        headers={
            "Content-Type" : "text/csv",
            "Content-Disposition" : f"attachment; filename={filename}",
        }
    )





# !!!!!!!!! running the app !!!!!!!!!!

# to get a free port
def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]

# the running function
if __name__ == "__main__":
    num = get_free_port()
    print(f" * Starting Flask on the Free Port : {num}")
    app.run(debug=True, port=num)
