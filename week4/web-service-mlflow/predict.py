import os
import pickle

import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify

MLFLOW_TRACKING_URI = "http://localhost:5000"
RUN_ID = os.getenv("RUN_ID", "2925de95bb794eee9169807dba9bf3fd")

client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

path = client.download_artifacts(run_id=RUN_ID, path="dict_vectorizer.bin")
print(f"Downloaded artifact to: {path}")

with open(path, "rb") as f_out:
    dv = pickle.load(f_out)

# Load model as a PyFuncModel.
logged_model = f"s3://kade-mlflow-artifacts/1/{RUN_ID}/artifacts/model"
model = mlflow.pyfunc.load_model(logged_model)


def prepare_features(ride):
    features = {}
    features["PU_DO"] = f"{ride['PULocationID']}_{ride['DOLocationID']}"
    features["trip_distance"] = ride["trip_distance"]
    return features


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]


app = Flask("duration-prediction")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {"duration": pred, "model_version": RUN_ID}

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
