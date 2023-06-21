import pickle
import sys
import pandas as pd

CATEGORICAL_COLUMNS = ["PULocationID", "DOLocationID"]


def load_model():
    with open("model.bin", "rb") as f_in:
        dv, model = pickle.load(f_in)

    return dv, model


def read_data(filename):
    df = pd.read_parquet(filename)

    df["duration"] = df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    df["duration"] = df["duration"].dt.total_seconds() / 60

    df = df[(df["duration"] > 0) & (df["duration"] <= 60)].copy()

    df[CATEGORICAL_COLUMNS] = df[CATEGORICAL_COLUMNS].fillna(-1).astype(int).astype(str)

    return df


def get_paths(year, month):
    input_path = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        + f"yellow_tripdata_{year:04d}-{month:02d}.parquet"
    )
    output_path = f"yellow_tripdata_{year:04d}-{month:02d}.parquet"

    return input_path, output_path


def apply_model(df):
    dicts = df[CATEGORICAL_COLUMNS].to_dict(orient="records")

    dv, model = load_model()

    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    print(f"the mean duration is {y_pred.mean():.2f}")

    return y_pred


def get_ride_id(year, month, df):
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")
    return df["ride_id"]


def save_results(df, y_pred, output_file):
    df_result = pd.DataFrame()

    df_result["ride_id"] = df["ride_id"]
    df_result["prediction"] = y_pred

    df_result.to_parquet(
        output_file,
        engine="pyarrow",
        compression=None,
        index=False,
    )


def run(year, month):
    input_file, output_file = get_paths(year, month)
    df = read_data(input_file)

    df["ride_id"] = get_ride_id(year, month, df)

    y_pred = apply_model(df)

    save_results(df, y_pred, output_file)


if __name__ == "__main__":
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    run(year, month)
