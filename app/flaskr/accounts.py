from flask import Blueprint, request, abort, jsonify
from . import business

bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@bp.route("/create", methods=['POST'])
def create_account():
    return {
        "account_number": business.create_account()
    }


@bp.route("/<account_number>/balance", methods=['GET'])
def get_balance(account_number):

    verifyAccountExists(account_number)

    return {
        "balance": business.get_balance(account_number)
    }


@bp.route("/<account_number>/deposit", methods=['PUT'])
def deposit_to_account(account_number):

    sum = parseTransactionSum(request.args['sum'])
    verifyAccountExists(account_number)

    return {
        "balance": business.deposit_to_account(account_number, sum)
    }


@bp.route("/<account_number>/withdraw", methods=['PUT'])
def withdraw_from_account(account_number):

    sum = parseTransactionSum(request.args['sum'])
    verifyAccountExists(account_number)

    return {
        "balance": business.withdraw_from_account(account_number, sum)
    }

# REQUEST CHECKERS


def parseTransactionSum(sum):
    try:
        return int(sum)
    except:
        abort(400, description="transaction sum is invalid")


def verifyAccountExists(account_number):
    if not business.does_account_exist(account_number):
        abort(404, description="account does not exist")

# ERROR HANDLERS


@bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e.description)), 404


@bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400
