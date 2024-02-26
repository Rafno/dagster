from dagster import Definitions

from .assets import core_asset

all_assets = [*core_asset]

defs = Definitions(
    assets=all_assets,
)
