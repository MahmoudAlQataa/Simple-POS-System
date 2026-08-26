import sys
import os
from flask import Flask

from extensions import db
from routes import main_bp
# from services import get_free_port
from services import get_local_ip
from flask_migrate import Migrate
import config


def create_app():
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    else:
        app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mahmoud-test-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    os.makedirs(config.INSTANCE_DIR, exist_ok=True)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_network_info():
        return {
            "local_ip": get_local_ip(),
            "app_port": config.PORT,
        }

    return app


app = create_app()


# if __name__ == "__main__":
#     num = get_free_port()
#     print(f" * Starting Flask on the Free Port : {num}")
#     app.run(debug=True, port=num)
if __name__ == "__main__":
    from models import AuthSettings

    with app.app_context():
        if not AuthSettings.query.first():
            default_auth = AuthSettings(
                admin_password=config.ADMIN_PASSWORD,
                worker_password=config.WORKER_PASSWORD,
            )
            db.session.add(default_auth)
            db.session.commit()

    print(f" * Starting Flask on port {config.PORT} (accessible from local network)")
    app.run(debug=True, host="0.0.0.0", port=config.PORT)