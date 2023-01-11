import pytest 
from bs4 import BeautifulSoup

from app import app as flask_app

@pytest.fixture()
def app():
    app = flask_app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_post(client):
    response = client.post('/testing', data={'name':'go to gym'})
    x = BeautifulSoup(response.data, 'html.parser').p
    x.attrs.pop('class')
    y = BeautifulSoup('<p>go to gym</p>', 'html.parser').p
    assert x == y

