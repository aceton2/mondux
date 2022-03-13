import time
from . import db_connect


def create_account():
    account_number = str(time.time()*1000)[:13]
    db_connect.create_account(account_number)
    return account_number


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
