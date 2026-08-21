import sys
import os

if getattr(sys, 'frozen', False):
    # جوا الـ exe المُغلّف
    BASE_DIR = os.path.dirname(sys.executable)
    BUNDLE_DIR = sys._MEIPASS
else:
    # بالتطوير (python app.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BUNDLE_DIR = BASE_DIR

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.environ.get("POS_DB_PATH") or os.path.join(INSTANCE_DIR, "expenses.db")
REPORTS_DIR = os.path.join(INSTANCE_DIR, "reports")
EXPORTS_DIR = os.path.join(INSTANCE_DIR, "exports")
BILS_REPORTS_DIR = os.path.join(INSTANCE_DIR, "Bils")
BACKUP_DIR = os.path.join(os.path.dirname(BASE_DIR), "Backups")

WKHTMLTOPDF_PATH = os.path.join(BUNDLE_DIR, "bin", "wkhtmltopdf.exe")

# ثابت (مش عشوائي) عشان يمكن الوصول من الجوال بنفس الرقم كل مرة
PORT = 5000
