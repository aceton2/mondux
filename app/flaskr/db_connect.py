from flask import g, current_app
import psycopg2


def init_db(app):
    create_table()
    app.teardown_appcontext(close_db)


def get_conn():
    if 'conn' not in g:
        g.conn = psycopg2.connect(**current_app.config['DATABASE'])

    return g.conn


def close_db(e=None):
    conn = g.pop('conn', None)
    if conn is not None:
        conn.close()


def run_query(query, data=None, fetch=False):
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query, data)
            if fetch:
                return cursor.fetchall()


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
    data = run_query(
        "SELECT * FROM accounts WHERE account_number = %s;", (account_number,), True)

    if data is None:
        return None
    else:
        return data[0][2]
