from io import BytesIO

import pandas as pd
import requests

from dagster import AssetExecutionContext, AssetMaterialization, MetadataValue, asset


@asset
def read_five(context):
    return None
