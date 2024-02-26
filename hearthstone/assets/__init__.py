from dagster import load_assets_from_package_module

from . import fetchcards

core_asset = load_assets_from_package_module(
    package_module=fetchcards, group_name="hearthstone_extract"
)
