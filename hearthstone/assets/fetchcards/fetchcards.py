from io import BytesIO

import duckdb
import pandas as pd
import requests
from pandas import DataFrame

from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue, asset

from . import hearthstone_api


@asset
def get_hearthstone_cards_asset(context):
    deck = hearthstone_api.get_all_hearthstone_cards(context)
    first_card = deck["cards"][0]
    context.log.info(first_card)

    markdown_list = "\n".join([f"- {key}" for key in first_card.keys()])

    metadata_dict = {
        "row_count": len(deck),
        "key_values": MetadataValue.md(markdown_list),
        "image_url": MetadataValue.md(f"![Card Image]({first_card['image']['en_US']})"),
        "json_example": MetadataValue.md(str(first_card)),
    }
    context.add_output_metadata(metadata=metadata_dict)
    return deck


def flatten_json(nested_json, exclude=[""]):
    """Flatten json object with nested keys into a single level.
    Args:
        nested_json: A nested json object.
        exclude: Keys to exclude from output.
    Returns:
        The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name="", exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude:
                    flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


@asset()
def flatten_cards_asset(context, get_hearthstone_cards_asset):
    deck = get_hearthstone_cards_asset
    df = pd.DataFrame([flatten_json(x) for x in deck["cards"]])
    context.log.info(df)

    # Convert DataFrame to Markdown
    markdown_str = df.head(5).to_markdown()  # Convert first 5 rows to Markdown

    # Log metadata and materialize the asset
    metadata_dict = {
        # "column_names": list(df.columns),
        "row_count": len(df),
        "preview": MetadataValue.md(markdown_str),
    }
    context.add_output_metadata(metadata=metadata_dict)
    context.log.info("Exported DataFrame to Markdown format")
