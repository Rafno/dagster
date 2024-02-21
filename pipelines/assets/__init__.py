from dagster import Definitions, load_assets_from_modules

from . import medicine_assets, raw_data_assets

all_assets = load_assets_from_modules([medicine_assets, raw_data_assets])

defs = Definitions(
    assets=all_assets,
)
