FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

COPY pyproject.toml setup.cfg setup.py /opt/dagster/dagster_home/

COPY medicine /opt/dagster/dagster_home/medicine

WORKDIR /opt/dagster/dagster_home

RUN pip install .

EXPOSE 3000

ENTRYPOINT ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]
