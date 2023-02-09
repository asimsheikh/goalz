import pytest 
from bs4 import BeautifulSoup

from flask import Response
from app import app as flask_app

@pytest.fixture()
def app():
    app = flask_app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_post(client):
    response: Response = client.post('/testing', data={'name':'go to gym'})
    if not response.status_code == 200: 
        raise Exception

    x = BeautifulSoup(response.data, 'html.parser').p
    x.attrs.pop('class') if 'class' in x.attrs else ''
    y = BeautifulSoup('<p>help to gym</p>', 'html.parser').p
    assert x == y

def test_add_comment(client):

    data = { 'action': 'add_comment', 'payload': {'date': '07-02-2023', 'comment': 'We are winning'} }
    response: Response = client.post('/testing', json=data)
    assert response.json == data['payload']
    # assert response.data == b'<p>Comment</p>'