import pytest 
from bs4 import BeautifulSoup
from datetime import datetime 

from flask import Response
from app import app as flask_app
from app import to_datetime, to_js_date

@pytest.fixture()
def app():
    app = flask_app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

# def test_post(client):
#     response: Response = client.post('/testing', data={'name':'go to gym'})
#     if not response.status_code == 200: 
#         raise Exception

#     x = BeautifulSoup(response.data, 'html.parser').p
#     x.attrs.pop('class') if 'class' in x.attrs else ''
#     y = BeautifulSoup('<p>help to gym</p>', 'html.parser').p
#     assert x == y

def test_add_comment(client):
    comment = 'Hello KL'
    data = { 'action': 'add_comment', 
             'payload': {
                'date': '07-02-2023', 
                'comment': comment} 
            }
    response: Response = client.post('/testing', json=data)
    assert response.data == f'<p>{comment}</p>'.encode()

def test_parse_to_datetime():
    js_date = "2023-02-09t00:00:00.000z"
    date = to_datetime(js_date=js_date)
    assert date == datetime(2023,2,9)

def test_datetime_to_js_date():
    js_date_str = "2022-01-01T00:00:00Z"
    assert to_js_date(datetime(2022,1,1,0, 0, 0, 0)) == js_date_str
