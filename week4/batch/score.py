import os
import sys
import uuid

import mlflow
import pandas as pd


def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids


def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df["ride_id"] = generate_uuids(len(df))
    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    df["PU_DO"] = df["PULocationID"] + "_" + df["DOLocationID"]
    categorical = ["PU_DO"]
    numerical = ["trip_distance"]
    dicts = df[categorical + numerical].to_dict(orient="records")

    return dicts


def load_model(run_id):
    logged_model = f"s3://kade-mlflow-artifacts/1/{run_id}/artifacts/model"
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def apply_model(input_file, run_id, output_file):
    print(f"reading {input_file}...")
    df = read_dataframe(input_file)

    dicts = prepare_dictionaries(df)

    print(f"loading model {run_id}...")
    model = load_model(run_id)

    print("applying the model...")
    y_pred = model.predict(dicts)

    print(f"saving the results to {output_file}...")
    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["lpep_pickup_datetime"] = df["lpep_pickup_datetime"]
    df_result["PULocationID"] = df["PULocationID"]
    df_result["DOlocationID"] = df["DOLocationID"]
    df_result["actual_duration"] = df["duration"]
    df_result["predicted_duration"] = y_pred
    df_result["diff"] = df_result["actual_duration"] - df_result["predicted_duration"]
    df_result["model_version"] = run_id

    df_result.to_parquet(output_file, index=False)


def run():
    taxi_type = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    input_file = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        + f"{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
    )
    output_file = f"output/{taxi_type}/{year:04d}-{month:02d}.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    os.environ["AWS_DEFAULT_PROFILE"] = "my-kade"
    RUN_ID = os.getenv("RUN_ID", "abf2e9dc119f4aa5baeffcce17ec7a83")

    apply_model(input_file, RUN_ID, output_file)


if __name__ == "__main__":
    run()
