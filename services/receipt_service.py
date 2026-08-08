import os
import pdfkit
from flask import render_template
from models.tests import Test

# مسار wkhtmltopdf على جهاز Mahmoud
WKHTMLTOPDF_PATH = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

PDFKIT_OPTIONS = {
    'encoding': 'UTF-8',
    'margin-top': '6cm',   # فراغ فوق للترويسة المطبوعة مسبقاً
    'margin-bottom': '1cm',
    'margin-left': '1cm',
    'margin-right': '1cm',
}


def _get_tests_list(expense):
    """
    بتفكك expense.category (نص فيه أسماء التحاليل مفصولة بـ ', ')
    وبتربط كل اسم بسعره الفعلي من جدول Test.
    """
    if not expense.category:
        return []

    test_names = [name.strip() for name in expense.category.split(",") if name.strip()]

    tests_list = []
    for name in test_names:
        test = Test.query.filter_by(name=name).first()
        if test:
            tests_list.append(test)
        else:
            # لو التحليل انحذف لاحقاً من جدول Test بعد ما اتسجلت فيه العملية
            # بنعرضه بالوصل بسعر 0 عشان ما يختفي الاسم من السند القديم
            fake_test = Test(name=name, price=0.0)
            tests_list.append(fake_test)

    return tests_list


def _get_receipt_path(expense):
    """
    بترجع مسار الملف الكامل بناءً على تاريخ العملية نفسها:
    instance/reports/<year>/<month>/receipt_<id>.pdf
    """
    year = expense.date.year
    month = expense.date.month

    folder = os.path.join("instance", "reports", str(year), str(month))
    os.makedirs(folder, exist_ok=True)

    filename = f"receipt_{expense.id}.pdf"
    return os.path.join(folder, filename)


def generate_receipt(expense):
    """
    بتولّد (أو تعيد توليد) ملف PDF لسند القبض تبع عملية معينة.
    """
    tests_list = _get_tests_list(expense)

    html = render_template(
        "receipt.html",
        expense=expense,
        tests_list=tests_list,
    )

    path = _get_receipt_path(expense)

    try:
        pdfkit.from_string(html, path, configuration=PDFKIT_CONFIG, options=PDFKIT_OPTIONS)
    except OSError:
        # غالباً السبب إنه الملف مفتوح ببرنامج PDF viewer وقت محاولة الكتابة عليه
        raise RuntimeError(
            "تم حفظ التعديل بنجاح، لكن تعذر تحديث ملف الوصل لأنه مفتوح ببرنامج آخر. "
            "أغلق الملف واضغط حفظ مرة أخرى لتحديث الوصل."
        )

    return path


def delete_receipt(expense):
    """
    بتحذف ملف الوصل المرتبط بعملية معينة لو موجود.
    """
    path = _get_receipt_path(expense)
    if os.path.exists(path):
        os.remove(path)
        
def open_receipt(expense):
    """
    بتفتح ملف الوصل تبع عملية معينة بالبرنامج الافتراضي (PDF viewer).
    """
    path = _get_receipt_path(expense)
    if os.path.exists(path):
        os.startfile(path)
        return True
    return False