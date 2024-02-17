import os

from dagster import (
    Definitions,
    FilesystemIOManager,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from .assets import raw_data

raw_data_assets = load_assets_from_package_module(
    raw_data,
    group_name="raw_data",
    key_prefix=["raw_data"],
)


everything_job = define_asset_job("everything_everywhere_job", selection="*")


defs = Definitions(
    assets=[*raw_data_assets],
)