from setuptools import find_packages, setup

setup(
    name="medicine",
    packages=find_packages(where=".", exclude=["medicine_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-webserver",
        "openpyxl",
        "pandas",
    ],
    extras_require={"dev": ["duckdb", "pytest"]},
)
