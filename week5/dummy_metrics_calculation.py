import datetime
import time
import random
import logging
import uuid
import pytz
import io

import pandas as pd
import psycopg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics (
    timestamp timestamp,
    value1 integer,
    value2 varchar,
    value3 float
);
"""


def prep_db():
    # check the docker compose
    with psycopg.connect(
        "host=localhost port=5432 user=postgres password=example",
        autocommit=True,
    ) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("CREATE DATABASE test;")

        with psycopg.connect(
            "host=localhost port=5432 user=postgres password=example dbname=test"
        ) as conn:
            conn.execute(create_table_statement)


def calculate_dummy_metrics_postgresql(curr):
    value1 = rand.randint(0, 1000)
    value2 = str(uuid.uuid4())
    value3 = rand.random()

    curr.execute(
        "INSERT INTO dummy_metrics (timestamp, value1, value2, value3) VALUES (%s, %s, %s, %s)",  # noqa
        (datetime.datetime.now(pytz.timezone("Europe/London")), value1, value2, value3),
    )


def main():
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)

    with psycopg.connect(
        "host=localhost port=5432 user=postgres password=example dbname=test",
        autocommit=True,
    ) as conn:
        for i in range(100):
            with conn.cursor() as curr:
                calculate_dummy_metrics_postgresql(curr)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send += datetime.timedelta(seconds=10)
            logging.info("Sent %s rows", i + 1)


if __name__ == "__main__":
    main()
