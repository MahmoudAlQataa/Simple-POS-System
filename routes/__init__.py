from flask import Blueprint

main_bp = Blueprint("main", __name__)

# Importing the route modules registers their view functions
# onto main_bp (each module does @main_bp.route(...)).
from routes import login  # noqa: E402,F401
from routes import index  # noqa: E402,F401
from routes import add  # noqa: E402,F401
from routes import delete  # noqa: E402,F401
from routes import edit  # noqa: E402,F401
from routes import settings  # noqa: E402,F401
from routes import add_test  # noqa: E402,F401
from routes import delete_test  # noqa: E402,F401
from routes import export  # noqa: E402,F401
from routes import data  # noqa: E402,F401
from routes import receipt  # noqa: E402,F401
from routes import bils  # noqa: E402,F401
from routes import add_bil  # noqa: E402,F401
from routes import edit_bil  # noqa: E402,F401
from routes import delete_bil  # noqa: E402,F401
from routes import receipt_bil  # noqa: E402,F401
from routes import customer_search  # noqa: E402,F401
from routes import customer  # noqa: E402,F401
from routes import edit_customer  # noqa: E402,F401
from routes import customer_payment  # noqa: E402,F401
from routes import payment_receipt  # noqa: E402,F401
from routes import change_password  # noqa: E402,F401