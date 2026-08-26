from flask import request, redirect, url_for, flash
from routes import main_bp
from extensions import db
from models import AuthSettings
from services.auth_service import admin_required


@main_bp.route("/settings/change_password", methods=["POST"])
@admin_required
def change_password():
    target = request.form.get("target", "")
    old_password = request.form.get("old_password", "")
    new_password = request.form.get("new_password", "").strip()

    if target not in ("admin", "worker"):
        flash("لازم تحدد أي كلمة سر بدك تعدل", "error")
        return redirect(url_for("main.settings"))

    if not new_password:
        flash("كلمة السر الجديدة لازم تكون معبأة", "error")
        return redirect(url_for("main.settings"))

    auth_settings = AuthSettings.query.first()

    if target == "admin":
        if old_password != auth_settings.admin_password:
            flash("كلمة السر القديمة غير صحيحة", "error")
            return redirect(url_for("main.settings"))
        auth_settings.admin_password = new_password
        db.session.commit()
        flash("تم تحديث كلمة سر الـ Admin بنجاح", "success")
    else:  # worker
        if old_password != auth_settings.worker_password:
            flash("كلمة السر القديمة غير صحيحة", "error")
            return redirect(url_for("main.settings"))
        auth_settings.worker_password = new_password
        db.session.commit()
        flash("تم تحديث كلمة سر الـ Worker بنجاح", "success")

    return redirect(url_for("main.settings"))