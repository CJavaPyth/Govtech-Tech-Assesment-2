from cgi import test
from flask import Flask
from src.household import household
from src.database import Household, db
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI")
        )
    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)
    # app.register_blueprint(resident)
    app.register_blueprint(household)
    

    return app

# use blueprints to group related functionalities together
