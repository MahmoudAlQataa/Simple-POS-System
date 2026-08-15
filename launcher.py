import sys
import os
import threading
import time
import urllib.request
import socket
import pathlib
from services.backup_service import run_backup_if_needed
import config

PORT = config.PORT

# Redirect streams عند التشغيل كـ exe مغلف (يمنع كسر المكتبات لما console=False)
if getattr(sys, 'frozen', False):
    log_path = pathlib.Path(os.path.dirname(sys.executable)) / "app_log.txt"
    sys.stdout = open(log_path, 'w', encoding='utf-8')
    sys.stderr = sys.stdout

    # تأكد إن الـ working directory صح (جنب الـ exe)
    os.chdir(os.path.dirname(sys.executable))

# def get_free_port():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(('127.0.0.1', 0))
#         return s.getsockname()[1]


# PORT = get_free_port()


def run_flask():
    from app import app
    from flask_migrate import upgrade
    import config

    migrations_dir = os.path.join(config.BUNDLE_DIR, "migrations")

    with app.app_context():
        upgrade(directory=migrations_dir)
    # app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)


flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

threading.Thread(target=run_backup_if_needed, daemon=True).start()

for _ in range(40):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}", timeout=1)
        break
    except:
        time.sleep(0.5)

import webview

window = webview.create_window(
    title="MyLap - مختبري", 
    url=f"http://127.0.0.1:{PORT}",
    width=1280,
    height=800,
    resizable=True,
)

webview.start()
