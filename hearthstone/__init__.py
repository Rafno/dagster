from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import core_asset
import os
all_assets = [*core_asset]
from .constants import dbt_project_dir

defs = Definitions(
    assets=all_assets,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)
