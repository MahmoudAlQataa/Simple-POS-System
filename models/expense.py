from datetime import date
from extensions import db


# Define the Expense table (model).
class Expense(db.Model):
    #__tablename__ = "Expense" # if you want to spicefai the tabel name
    # intialising the columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False, default=0.0)
    paid_amount = db.Column(db.Float, nullable=False)
    remain_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    gender = db.Column(db.String(10), nullable=False)
    doctor_name = db.Column(db.String(50), nullable=True)