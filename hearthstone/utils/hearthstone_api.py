import requests
from dotenv import load_dotenv
import os

def get_hearthstone_cards():
    url = "https://us.api.blizzard.com/hearthstone/cards"
    params = {
        "locale": "en_US",
        "access_token": __get_access_token()
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_access_token():
    load_dotenv()

    # Access environment variables
    BATTLENET_CLIENT_ID = os.getenv("BATTLENET_CLIENT_ID")
    BATTLENET_CLIENT_SECRET = os.getenv("BATTLENET_CLIENT_SECRET")
    return BATTLENET_CLIENT_ID, BATTLENET_CLIENT_SECRET


