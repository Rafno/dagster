from dagster import load_assets_from_package_module

from . import fetchmeds, testmodule

core_asset = load_assets_from_package_module(
    package_module=fetchmeds, group_name="meds"
)

test_asset = load_assets_from_package_module(
    package_module=testmodule, group_name="testing"
)
