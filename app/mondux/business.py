import time
from . import db_connect


def create_account():
    account_number = create_account_number()
    db_connect.create_account(account_number)
    return account_number


def does_account_exist(account_number):
    balance = db_connect.get_balance(account_number)
    return False if balance is None else True


def get_balance(account_number):
    return db_connect.get_balance(account_number)


def withdraw_from_account(account_number, amount):
    balance = db_connect.get_balance(account_number)
    new_balance = balance - amount
    db_connect.update_balance(account_number, new_balance)
    return new_balance


def deposit_to_account(account_number, amount):
    balance = db_connect.get_balance(account_number)
    new_balance = balance + amount
    db_connect.update_balance(account_number, new_balance)
    return new_balance


def create_account_number():
    return str(time.time()*1000)[:13]
