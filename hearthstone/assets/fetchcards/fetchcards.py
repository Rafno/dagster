import os
from io import BytesIO

import duckdb
import pandas as pd
import requests
from dagster_dbt import DbtCliResource, dbt_assets
from pandas import DataFrame

from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue, asset

from ...constants import dbt_manifest_path, dbt_project_dir
from . import hearthstone_api

duckdb_database_path = dbt_project_dir.joinpath("tutorial.duckdb")


@asset(compute_kind="python")
def get_hearthstone_cards_asset(context):
    deck = hearthstone_api.get_all_hearthstone_cards(context)
    context.log.info(deck)
    first_card = deck[0]
    context.log.info(first_card)

    markdown_list = "\n".join([f"- {key}" for key in first_card.keys()])

    metadata_dict = {
        "row_count": len(deck),
        "key_values": MetadataValue.md(markdown_list),
        "image_url": MetadataValue.md(f"![Card Image]({first_card['image']['en_US']})"),
        "json_example": MetadataValue.md(str(first_card)),
    }
    context.add_output_metadata(metadata=metadata_dict)

    flat_deck = pd.DataFrame([flatten_json(x) for x in deck])

    return flat_deck


@asset(compute_kind="python")
def get_hearthstone_metadata_asset(context):
    metadata = hearthstone_api.get_all_hearthstone_metadata(context)
    context.log.info(metadata["classes"])
    flat_deck = pd.DataFrame([flatten_json(x) for x in metadata])

    return flat_deck


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


@asset(compute_kind="python")
def raw_cards(context, get_hearthstone_cards_asset):
    deck = get_hearthstone_cards_asset
    connection = duckdb.connect(os.fspath(duckdb_database_path))
    connection.execute("SET GLOBAL pandas_analyze_sample=100000")
    connection.execute("create schema if not exists api")
    connection.execute("create or replace table api.raw_cards as select * from deck")

    # Log some metadata about the table we just wrote. It will show up in the UI.
    context.add_output_metadata({"num_rows": deck.shape[0]})


@asset(compute_kind="python")
def raw_metadata(context, raw_cards, get_hearthstone_metadata_asset):
    deck = get_hearthstone_metadata_asset
    connection = duckdb.connect(os.fspath(duckdb_database_path))
    connection.execute("SET GLOBAL pandas_analyze_sample=100000")
    connection.execute("create schema if not exists api")
    connection.execute("create or replace table api.raw_classes as select * from deck")

    # Log some metadata about the table we just wrote. It will show up in the UI.
    context.add_output_metadata({"num_rows": deck.shape[0]})


@dbt_assets(manifest=dbt_manifest_path)
def card_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
