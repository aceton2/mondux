from flaskr import db_connect


def test_single_db_connection(app):
    with app.app_context():
        conn = db_connect.get_conn()
        assert conn is db_connect.get_conn()
