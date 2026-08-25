from flask import request, jsonify
from routes import main_bp
from models import Customer
from services.auth_service import login_required

@main_bp.route("/customer/search")
@login_required
def customer_search():
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify([])

    customers = Customer.query.filter(Customer.name.ilike(f"%{q}%")).limit(10).all()

    results = [
        {"id": c.id, "name": c.name, "phone": c.phone or "", "gender": c.gender}
        for c in customers
    ]
    return jsonify(results)