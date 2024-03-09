import os

import requests
from dotenv import load_dotenv

from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue
from ...constants import BATTLENET_CLIENT_ID, BATTLENET_CLIENT_SECRET


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


def get_all_hearthstone_cards(context) -> list:
    reqUrl = "https://eu.api.blizzard.com/hearthstone/cards/"
    token = generate_bearer_token(context, BATTLENET_CLIENT_ID, BATTLENET_CLIENT_SECRET)

    headersList = {
        "Accept": "*/*",
        "User-Agent": "application/json",
        "Authorization": f"bearer {token}",
    }

    all_cards = []  # List to store all fetched cards


    page = 1
    while True:
        context.log.info(f"Fetching page {page}")
        response = requests.get(reqUrl, headers=headersList)
        context.log.info(f"status code was {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            all_cards.extend(data["cards"])  # Append fetched cards to the list

            # Check if there are more pages
            if page >= data["pageCount"]:
                break  # Exit loop if reached last page

            page += 1  # Move to the next page
        else:
            context.log.error("Failed to fetch hearthstone cards")
            return None

    return all_cards
