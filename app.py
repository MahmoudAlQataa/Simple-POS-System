import sys
import os
from flask import Flask

from extensions import db
from routes import main_bp
from services import get_free_port
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

    return app


app = create_app()


if __name__ == "__main__":
    num = get_free_port()
    print(f" * Starting Flask on the Free Port : {num}")
    app.run(debug=True, port=num)