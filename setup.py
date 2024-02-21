import glob

from setuptools import find_packages, setup

setup(
    name="testing_dagster",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "boto3",
        "dagster-dbt",
        "pandas",
        "numpy",
        "scipy",
        "dbt-core",
        "dbt-duckdb",
        "dagster-duckdb",
        "dagster-webserver",
        "dagster-duckdb-pandas",
        # packaging v22 has build compatibility issues with dbt as of 2022-12-07
        "packaging<22.0",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
