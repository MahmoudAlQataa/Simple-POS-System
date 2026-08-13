import os
import pdfkit
from flask import render_template
import config

PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=config.WKHTMLTOPDF_PATH)

PDFKIT_OPTIONS = {
    'encoding': 'UTF-8',
    'margin-top': '6cm',
    'margin-bottom': '1cm',
    'margin-left': '1cm',
    'margin-right': '1cm',
}


def _get_receipt_path(bil):
    year = bil.bil_date.year
    month = bil.bil_date.month

    folder = os.path.join(config.BILS_REPORTS_DIR, str(year), str(month))
    os.makedirs(folder, exist_ok=True)

    filename = f"bil_{bil.bil_id}.pdf"
    return os.path.join(folder, filename)


def generate_bil_receipt(bil):
    html = render_template("bil_receipt.html", bil=bil)
    path = _get_receipt_path(bil)

    try:
        pdfkit.from_string(html, path, configuration=PDFKIT_CONFIG, options=PDFKIT_OPTIONS)
    except OSError:
        raise RuntimeError(
            "تم حفظ التعديل بنجاح، لكن تعذر تحديث ملف الوصل لأنه مفتوح ببرنامج آخر. "
            "أغلق الملف واضغط حفظ مرة أخرى لتحديث الوصل."
        )

    return path


def delete_bil_receipt(bil):
    path = _get_receipt_path(bil)
    if os.path.exists(path):
        os.remove(path)


def open_bil_receipt(bil):
    path = _get_receipt_path(bil)
    if os.path.exists(path):
        os.startfile(path)
        return True
    return False