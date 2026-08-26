from extensions import db


# جدول فيه صف واحد بس (id=1) — بيخزن كلمتي السر الحاليتين للـ admin والـ worker
class AuthSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_password = db.Column(db.String(120), nullable=False)
    worker_password = db.Column(db.String(120), nullable=False)