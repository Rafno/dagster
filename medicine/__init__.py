from dagster import Definitions, load_assets_from_modules

from .assets import core_asset, trash_asset

all_assets = [*core_asset, *trash_asset]

defs = Definitions(
    assets=all_assets,
)
