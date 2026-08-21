from extensions import db
from models import Expense


PAYMENT_CATEGORY = "دفعة على الحساب"


def apply_fifo_credit(customer_id):
    """
    Looks for surplus records (remain_amount > 0) belonging to this customer,
    and uses them to automatically pay down any outstanding invoices
    (remain_amount < 0), oldest surplus first / oldest debt first (FIFO).

    Returns a list of all Expense rows that were modified (so the caller
    can regenerate their receipts). Each returned row also gets a temporary
    attribute `_owed_before` (the price-discount at the moment BEFORE this
    function ran) attached to it, for reporting purposes.
    """
    surplus_records = (
        Expense.query
        .filter(
            Expense.customer_id == customer_id,
            Expense.remain_amount > 0,
        )
        .order_by(Expense.date.asc(), Expense.id.asc())
        .all()
    )

    if not surplus_records:
        return []

    outstanding = (
        Expense.query
        .filter(
            Expense.customer_id == customer_id,
            Expense.category != PAYMENT_CATEGORY,
            Expense.remain_amount < 0,
        )
        .order_by(Expense.date.asc(), Expense.id.asc())
        .all()
    )

    if not outstanding:
        return []

    affected = []
    debt_index = 0

    for surplus in surplus_records:
        available = surplus.remain_amount  # positive

        if not hasattr(surplus, "_owed_before"):
            surplus._owed_before = surplus.price - surplus.discount

        while available > 0 and debt_index < len(outstanding):
            invoice = outstanding[debt_index]
            owed = -invoice.remain_amount  # positive

            if not hasattr(invoice, "_owed_before"):
                invoice._owed_before = invoice.price - invoice.discount

            applied = min(owed, available)

            invoice.paid_amount += applied
            invoice.remain_amount = invoice.paid_amount - (invoice.price - invoice.discount)
            if invoice not in affected:
                affected.append(invoice)

            surplus.paid_amount -= applied
            surplus.remain_amount = surplus.paid_amount - (surplus.price - surplus.discount)
            if surplus not in affected:
                affected.append(surplus)

            available -= applied

            if invoice.remain_amount == 0:
                debt_index += 1

        if debt_index >= len(outstanding):
            break

    db.session.commit()
    return affected