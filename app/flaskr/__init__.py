from flask import Flask, request, render_template
from . import business


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        TEMPLATES_AUTO_RELOAD=True,
        DATABASE='config vars',
    )

    @app.route("/")
    def hello():
        return render_template('landing.html')

    @app.route("/api/accounts/create", methods=['POST'])
    def create_account():
        account_number = business.create_account()
        return {
            "account_number": account_number
        }

    @app.route("/api/accounts/<account_number>/balance", methods=['GET'])
    def get_balance(account_number):
        balance = business.get_balance(account_number)
        return {
            "balance": balance
        }

    @app.route("/api/accounts/<account_number>/deposit", methods=['PUT'])
    def deposit_to_account(account_number):
        sum = int(request.args['sum'])
        balance = business.deposit_to_account(account_number, sum)
        return {
            "balance": balance
        }

    @app.route("/api/accounts/<account_number>/withdraw", methods=['PUT'])
    def withdraw_from_account(account_number):
        sum = int(request.args['sum'])
        balance = business.withdraw_from_account(account_number, sum)
        return {
            "balance": balance
        }

    return app
