import os

import requests
from dotenv import load_dotenv

from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue


def __get_access_token():
    load_dotenv()

    # Access environment variables
    BATTLENET_CLIENT_ID = os.getenv("BATTLENET_CLIENT_ID")
    BATTLENET_CLIENT_SECRET = os.getenv("BATTLENET_CLIENT_SECRET")
    return BATTLENET_CLIENT_ID, BATTLENET_CLIENT_SECRET


def generate_bearer_token(context, client_id, client_secret) -> str:
    url = "https://us.battle.net/oauth/token"
    headersList = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"grant_type": "client_credentials"}
    response = requests.post(
        url, auth=(client_id, client_secret), data=payload, headers=headersList
    )

    if response.status_code == 200:
        token = response.json()["access_token"]
        context.log.info(f"generated token is {token}")
        return token
    else:
        context.log.error(f"failed to generate bearer token due to {response.text}")
        return None


def get_all_hearthstone_cards(context) -> str:
    reqUrl = "https://eu.api.blizzard.com/hearthstone/cards/"
    client_id, client_secret = __get_access_token()
    token = generate_bearer_token(context, client_id, client_secret)

    headersList = {
        "Accept": "*/*",
        "User-Agent": "application/json",
        "Authorization": f"bearer {token}",
    }

    payload = ""

    response = requests.get(reqUrl, data=payload, headers=headersList)
    context.log.info(f"status code was {response.status_code}")

    if response.status_code == 200:
        return response.json()
    else:
        context.log.error("Failed to fetch hearthstone cards")
        return None
