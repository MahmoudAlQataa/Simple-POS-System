from flask import Flask

from extensions import db
from routes import main_bp
from services import get_free_port
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mahmoud-test-key'  # a decode key for the cash data that stored in the setion

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'  # tell SQLAlchemy where the db is located
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stop the tracking we don't need it yet

    db.init_app(app)  # (Initialize SQLAlchemy) creat the db and connect it to the app
    migrate = Migrate(app, db)

    app.register_blueprint(main_bp)

    # with app.app_context():  # Enter the Flask application context. (# go in the env)
    #     db.create_all()  # Create all tables defined by the models (if they don't already exist).

    return app


app = create_app()


# !!!!!!!!! running the app !!!!!!!!!!
if __name__ == "__main__":
    num = get_free_port()
    print(f" * Starting Flask on the Free Port : {num}")
    app.run(debug=True, port=num)
