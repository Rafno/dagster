from hearthstone.utils.hearthstone_api import __get_access_token


def test_get_access_token():
    token, secret = __get_access_token()
    print(token, secret)
    assert True
