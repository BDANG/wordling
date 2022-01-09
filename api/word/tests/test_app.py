from chalice.test import Client
from app import app


def test_add_word():
    with Client(app) as client:
        result = client.http.post('/word')


def test_get_new_game():
    data = {'address': '0xmock'}
    with Client(app) as client:
        result = client.http.post('/game', json=data)


def test_get_new_game_after_solve():
    pass


def test_get_new_game_after_lost():
    pass


def test_get_existing_game():
    data = {'address': '0xmock'}
    with Client(app) as client:
        result = client.http.post('/game', json=data)
        result = client.http.post('/game', json=data)


def test_guess():
    data = {'address': '0xmock'}
    with Client(app) as client:
        result = client.http.post('/game', json=data)
        result = client.http.post('/game/guess', json=data)


def test_reguess():
    pass


def test_guess_beyond_6():
    pass


def test_word_check_exists():
    word = 'foob'
    with Client(app) as client:
        result = client.http.get(f'/word/{word}')


def test_word_check_not_exists():
    word = '0x0x0x0'
    with Client(app) as client:
        result = client.http.get(f'/word/{word}')