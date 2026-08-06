from flask import request, Response
import csv
import io

from routes import main_bp
from models import Expense
from services import parse_date_or_none


# export route
@main_bp.route("/export.csv")
def export_csv():
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    selected_category = (request.args.get("category") or "").strip()
    search_name = (request.args.get("search_name") or "").strip()
    show_outstanding = request.args.get("show_outstanding") == "1"
    show_overpaid = request.args.get("show_overpaid") == "1"

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    q = Expense.query

    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    if selected_category:
        q = q.filter(Expense.category.contains(selected_category))
    if search_name:
        q = q.filter(Expense.name.ilike(f"%{search_name}%"))
    if show_outstanding and show_overpaid:
        q = q.filter(Expense.remain_amount != 0)
    elif show_outstanding:
        q = q.filter(Expense.remain_amount < 0)
    elif show_overpaid:
        q = q.filter(Expense.remain_amount > 0)

    expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()

    # We use StringIO + csv.writer instead of building the string manually.
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["date", "name", "phone", "category", "price", "paid_amount", "remain_amount"])  # header row

    for e in expenses:  # data rows
        writer.writerow([
            e.date.isoformat(),
            e.name,
            e.phone,
            e.category,         # csv.writer automatically adds quotes if there are commas.
            f"{e.price:.2f}",
            f"{e.paid_amount:.2f}",
            f"{e.remain_amount:.2f}",
        ])

    csv_data = output.getvalue()

    fname_start = start_str or "all"
    fname_end = end_str or "all"
    filename = f"expenses_{fname_start}_to_{fname_end}.csv"

    return Response(
        csv_data,
        headers={
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename={filename}",
        }
    )
