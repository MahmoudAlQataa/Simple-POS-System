from datetime import date
from extensions import db

class Bils(db.Model):
    bil_id = db.Column(db.Integer, primary_key=True)
    bil_category = db.Column(db.String(50), nullable=False)
    campany = db.Column(db.String(50), nullable=False)
    bil_price = db.Column(db.Float, nullable=False)
    bil_paid_amount = db.Column(db.Float, nullable=True)
    bil_remain_amount = db.Column(db.Float, nullable=False)
    bil_date = db.Column(db.Date, nullable=False, default=date.today)
    