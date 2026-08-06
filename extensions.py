from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy instance, imported by models and app
# to avoid circular imports.
# (Initialize SQLAlchemy) creat the db and connect it to the app
db = SQLAlchemy()
