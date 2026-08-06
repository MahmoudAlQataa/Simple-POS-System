from datetime import date
from extensions import db


# Define the Expense table (model).
class Expense(db.Model):
    #__tablename__ = "Expense" # if you want to spicefai the tabel name
    # intialising the columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, nullable=False)
    remain_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)