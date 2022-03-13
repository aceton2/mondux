import psycopg2

# import os
# os.getenv("db_user")

dbconn = {'database': 'momo2',
          'user': 'postgres',
          'password': 'postgres',
          'host': 'pyth-db-1'}

conn = psycopg2.connect(**dbconn)
cur = conn.cursor()


def run_query(query, data=None):
    try:
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)


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
    run_query(
        "SELECT * FROM accounts WHERE account_number = %s;", (account_number,))
    data = cur.fetchall()
    if len(data) == 1:
        return data[0][2]
    else:
        return 0


# run this on start up
create_table()
