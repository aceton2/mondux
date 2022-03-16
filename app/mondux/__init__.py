import os
from flask import Flask, render_template
from . import accounts
from . import db_connect


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Config

    app.config.from_mapping(
        SECRET_KEY='dev',
        TEMPLATES_AUTO_RELOAD=True,
        DATABASE={
            'database': os.getenv("API_DB"),
            'user': os.getenv("API_DB_USER"),
            'password': os.getenv("API_DB_PASSWORD"),
            'host': os.getenv("API_DB_HOST")
        }
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    # Landing Page

    @app.route("/")
    def hello():
        return render_template('landing.html')

    # Accounts API

    app.register_blueprint(accounts.bp)

    # Database Init

    with app.app_context():
        db_connect.init_db(app)

    return app
