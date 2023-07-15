import os
import pandas as pd

from batch import main, get_input_path
from tests.test_batch import dt

data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2), dt(1, 10)),
    (1, 2, dt(2, 2), dt(2, 3)),
    (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
]
columns = [
    "PULocationID",
    "DOLocationID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]
df_input = pd.DataFrame(data, columns=columns)
input_file = get_input_path(2022, 1)

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}

df_input.to_parquet(
    input_file,
    engine="pyarrow",
    compression=None,
    index=False,
    storage_options=options,
)

main(2022, 1)

# 3667
# predicted mean duration: 10.502483457575869
