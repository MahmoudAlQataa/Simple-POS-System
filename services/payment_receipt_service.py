import os
from datetime import date
import pdfkit
from flask import render_template
from models import Expense
import config

PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=config.WKHTMLTOPDF_PATH)

PDFKIT_OPTIONS = {
    'encoding': 'UTF-8',
    'margin-top': '2cm',
    'margin-bottom': '1cm',
    'margin-left': '1cm',
    'margin-right': '1cm',
}


def _get_open_balance_rows(customer_id):
    """
    كل سجلات الزبون يلي remain_amount < 0 (لسا مديونة)، مرتبة من الأقدم للأحدث.
    """
    return (
        Expense.query
        .filter(
            Expense.customer_id == customer_id,
            Expense.remain_amount < 0,
        )
        .order_by(Expense.date.asc(), Expense.id.asc())
        .all()
    )


def _get_receipt_path(customer_id):
    folder = os.path.join(config.REPORTS_DIR, "customers", str(customer_id))
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "payment_receipt.pdf")


def generate_payment_receipt(customer, affected=None):
    """
    بتولّد (أو تعيد توليد) كشف الدفعة الشامل لزبون معين —
    بيعرض كل الفواتير يلي تأثرت بآخر دفعة (affected)، بالإضافة لأي
    فواتير لسا مديونة (remain_amount < 0)، مدموجين بدون تكرار
    ومرتبين من الأقدم للأحدث.
    """
    still_owed = _get_open_balance_rows(customer.id)

    combined = {r.id: r for r in (affected or [])}
    for r in still_owed:
        combined[r.id] = r

    rows = sorted(combined.values(), key=lambda r: (r.date, r.id))

    total_owed = sum(r.remain_amount for r in rows if r.remain_amount < 0)
    total_surplus = sum(r.remain_amount for r in rows if r.remain_amount > 0)
    net_balance = sum(r.remain_amount for r in rows)

    html = render_template(
        "payment_receipt.html",
        customer=customer,
        rows=rows,
        total_owed=total_owed,
        total_surplus=total_surplus,
        net_balance=net_balance,
        generated_date=date.today(),
    )

    path = _get_receipt_path(customer.id)

    try:
        pdfkit.from_string(html, path, configuration=PDFKIT_CONFIG, options=PDFKIT_OPTIONS)
    except OSError:
        raise RuntimeError(
            "تم حفظ الدفعة بنجاح، لكن تعذر تحديث ملف الكشف الشامل لأنه مفتوح ببرنامج آخر. "
            "أغلق الملف وحاول فتحه مرة أخرى."
        )

    return path


def open_payment_receipt(customer):
    path = _get_receipt_path(customer.id)
    if os.path.exists(path):
        os.startfile(path)
        return True
    return False