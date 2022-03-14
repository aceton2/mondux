from flask import Flask, render_template
from . import accounts
from . import db_connect


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        TEMPLATES_AUTO_RELOAD=True,
        DATABASE='config vars',
    )

    @app.route("/")
    def hello():
        return render_template('landing.html')

    app.register_blueprint(accounts.bp)

    with app.app_context():
        db_connect.init_db(app)

    return app
