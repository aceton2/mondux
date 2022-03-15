
# BASIC FUNCTIONALITY

def test_create_get(client):

    response_create = client.post('api/accounts/create')
    account_number = response_create.json["account_number"]
    response_balance1 = client.get(f'api/accounts/{account_number}/balance')

    assert response_balance1.json["balance"] == 0


def test_create_withdraw_get(client):

    response_create = client.post('api/accounts/create')
    account_number = response_create.json["account_number"]

    client.put(f'api/accounts/{account_number}/withdraw?sum=20')
    response_balance = client.get(f'api/accounts/{account_number}/balance')

    assert response_balance.json["balance"] == -20


def test_create_deposit_get(client):

    response_create = client.post('api/accounts/create')
    account_number = response_create.json["account_number"]

    client.put(f'api/accounts/{account_number}/deposit?sum=20')
    response_balance2 = client.get(f'api/accounts/{account_number}/balance')

    assert response_balance2.json["balance"] == 20


# ACCOUNT DOES NOT EXIST

def test_get_balance_of_invalid(client):
    res = client.get(f'api/accounts/unknown_account/balance')
    assert res.status_code == 404


def test_make_deposit(client):
    res = client.put(f'api/accounts/unknown_account/deposit?sum=123')
    assert res.status_code == 404


def test_make_withdrawl(client):
    res = client.put('api/accounts/unknown_account/withdraw?sum=123')
    assert res.status_code == 404

# SUM IS INVALID


def test_make_deposit(client):
    res = client.put(f'api/accounts/unknown_account/deposit?sum=1invalid')
    assert res.status_code == 400


def test_make_deposit(client):
    res = client.put(f'api/accounts/unknown_account/deposit?sum=1invalid')
    assert res.status_code == 400
