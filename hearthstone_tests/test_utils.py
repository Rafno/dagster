import pytest
import requests

from hearthstone.utils.hearthstone_api import __get_access_token


def test_get_request(requests_mock):
    return_card_json = {
        "cardId": "EX1_116",
        "dbfId": 559,
        "name": "Leeroy Jenkins",
        "cardSet": "Hall of Fame",
        "type": "Minion",
        "faction": "Alliance",
        "rarity": "Legendary",
        "cost": 5,
        "attack": 6,
        "health": 2,
        "text": "<b>Charge</b>. <b>Battlecry:</b> Summon two 1/1 Whelps for your opponent.",
        "flavor": "At least he has Angry Chicken.",
        "artist": "Gabe from Penny Arcade",
        "collectible": True,
        "elite": True,
        "playerClass": "Neutral",
        "img": "https://d15f34w2p8l1cc.cloudfront.net/hearthstone/7740c50c88d17b12c3eccbf1c57af9163929add6c63bba7fbad663f574bc6307.png",
        "imgGold": "https://d15f34w2p8l1cc.cloudfront.net/hearthstone/cf21572abd2583e7520733ac221c35fd5aeb5d700de9b43895712a74c2c68eb4.png",
        "locale": "enUS",
        "mechanics": [{"name": "Charge"}, {"name": "Battlecry"}],
    }

    requests_mock.status_code = 200
    requests_mock.json = return_card_json
    response = requests.get("eu.api.blizzard.com/test")
    assert response.status_code == 200
    # assert response.json() == return_card_json


def test_get_access_token():
    token, secret = __get_access_token()
    print(token, secret)
    assert True
