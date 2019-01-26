import app
from flask import json


access_token = ""
base_url = 'http://localhost:5000'


def test_super_simple():
    response = app.test_client().get(
        '/super_simple'
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['message'] == 'Hello from the Planetary API'


def test_user_create():
    assert False


def test_login():
    assert False


def test_create():
    assert False


def test_update():
    assert False


def test_delete():
    assert False
