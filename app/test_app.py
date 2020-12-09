#  docker-compose run api coverage run -m pytest --disable-warnings
#  docker-compose run api coverage report --omit=app/test_app.py -m

import pytest

from fastapi.testclient import TestClient

from tortoise.contrib.test import finalizer, initializer

from datetime import datetime

from app import app

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = "postgres://postgres:postgres@database:5432/test"
    initializer(["models"], db_url=db_url, app_label="models")
    request.addfinalizer(finalizer)


def test_a_searches():
    response = client.get("/searches/")
    assert response.status_code == 200, response.text


def test_b_add():
    response = client.post("/add", json={'search_phrase': 'test2', 'region': 'Москва'})
    assert response.status_code == 200, response.text

    search_id = response.json()['id']

    response = client.get("/stats?search_id={}&to_datetime={}".format(search_id, datetime.now()))
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1

    response = client.get("/stats/top/{}".format(search_id))
    assert response.status_code == 200, response.text
    assert len(response.json()) >= 1


def test_c_add_bad_region():
    response = client.post("/add", json={'search_phrase': 'test', 'region': 'HELLOWORLD'})
    assert response.status_code == 404, response.text