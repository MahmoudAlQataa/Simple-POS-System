import os
import shutil
from datetime import date
import config


def run_backup_if_needed():
    today_str = date.today().isoformat()
    today_folder = os.path.join(config.BACKUP_DIR, today_str)

    if os.path.exists(today_folder):
        return  # في نسخة اليوم أصلاً، ما في داعي نعمل شي

    # امسح أي نسخ قديمة (بدنا نسخة وحيدة بس محفوظة)
    if os.path.exists(config.BACKUP_DIR):
        for old_folder in os.listdir(config.BACKUP_DIR):
            old_path = os.path.join(config.BACKUP_DIR, old_folder)
            if old_path != today_folder:
                shutil.rmtree(old_path, ignore_errors=True)

    os.makedirs(today_folder, exist_ok=True)
    shutil.copy2(config.DB_PATH, os.path.join(today_folder, "expenses.db"))