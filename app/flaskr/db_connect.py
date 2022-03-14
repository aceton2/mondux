from flask import g
import psycopg2

# import os
# os.getenv("db_user")

dbconn = {'database': 'momo3',
          'user': 'flaskr',
          'password': 'flaskr',
          'host': 'pyth-db-1'}


def init_db(app):
    create_table()
    app.teardown_appcontext(close_db)


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(**dbconn)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# FIX THIS
def run_query(query, data=None):
    conn = get_db()
    cur = conn.cursor()

    try:
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)

        conn.commit()

    except Exception as e:
        conn.rollback()
        print('cursor exception', e)

    return cur


def create_table():
    run_query(
        "CREATE TABLE IF NOT EXISTS accounts (id serial PRIMARY KEY, account_number varchar, balance_cents integer);")


def create_account(account_number):
    run_query(
        "INSERT INTO accounts (account_number, balance_cents) VALUES (%s, 0);", (account_number,))


def update_balance(account_number, balance):
    run_query(
        "UPDATE accounts SET balance_cents = %s WHERE account_number = %s;", (balance, account_number))


def get_balance(account_number):
    cur = run_query(
        "SELECT * FROM accounts WHERE account_number = %s;", (account_number,))

    data = cur.fetchall()

    if len(data) == 1:
        return data[0][2]
    else:
        return None
