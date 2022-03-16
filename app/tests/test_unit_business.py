import pytest
from mondux import db_connect, business

# MOCKS


def mock_create_account_num():
    # mocked because it relies on time.time
    return '010'


def mock_create_account(account_number):
    return None


def mock_get_balance(account_number):
    if (account_number == 'existing_account'):
        return 250
    else:
        return None


def mock_update_balance(account_number, balance):
    return None


@pytest.fixture
def mock_db_connect(monkeypatch):
    monkeypatch.setattr(db_connect, 'create_account', mock_create_account)
    monkeypatch.setattr(db_connect, 'get_balance', mock_get_balance)
    monkeypatch.setattr(db_connect, 'update_balance', mock_update_balance)


@pytest.fixture
def mock_create_account_number(monkeypatch):
    monkeypatch.setattr(business, 'create_account_number',
                        mock_create_account_num)

# TESTS


def test_create_account(mock_db_connect, mock_create_account_number):
    assert business.create_account() == '010'


def test_get_balance(mock_db_connect):
    assert business.get_balance('random') == None
    assert business.get_balance('existing_account') == 250


def test_does_account_exist(mock_db_connect):
    assert business.does_account_exist('random') is False
    assert business.does_account_exist('existing_account') is True


def test_deposit_to_account(mock_db_connect):
    # we are not re-querying the database after the balance update is successful. Thats why we can expect
    # the correct amount, even though the get_balance mock always returns the same value
    assert business.deposit_to_account(
        'existing_account', 5) == 255

    # we are handling the check as to wether the account exists in the controller, so this is ok
    with pytest.raises(TypeError) as e:
        business.deposit_to_account('random', 5)


def test_withdraw_from_account(mock_db_connect):
    assert business.withdraw_from_account(
        'existing_account', 5) == 245

    with pytest.raises(TypeError) as e:
        assert business.withdraw_from_account('random', 5) is None
