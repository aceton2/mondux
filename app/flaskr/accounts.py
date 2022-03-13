from flask import Blueprint, request
from . import business

bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@bp.route("/create", methods=['POST'])
def create_account():
    account_number = business.create_account()
    return {
        "account_number": account_number
    }


@bp.route("/<account_number>/balance", methods=['GET'])
def get_balance(account_number):
    balance = business.get_balance(account_number)
    return {
        "balance": balance
    }


@bp.route("/<account_number>/deposit", methods=['PUT'])
def deposit_to_account(account_number):
    sum = int(request.args['sum'])
    balance = business.deposit_to_account(account_number, sum)
    return {
        "balance": balance
    }


@bp.route("/<account_number>/withdraw", methods=['PUT'])
def withdraw_from_account(account_number):
    sum = int(request.args['sum'])
    balance = business.withdraw_from_account(account_number, sum)
    return {
        "balance": balance
    }
