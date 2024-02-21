from dagster import Definitions, load_assets_from_modules

from .assets import *

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
)
