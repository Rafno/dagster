from hearthstone.utils import get_access_token


def test_get_access_token():
    token, secret = get_access_token()
    print(token, secret)
