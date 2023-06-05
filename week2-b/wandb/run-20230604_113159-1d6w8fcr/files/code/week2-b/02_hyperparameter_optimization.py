import os
import pickle

import pandas as pd
import wandb

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


def run_train():
    wandb.init()

    # wandb sweep server에서 보내는 config
    config = wandb.config

    artifact = wandb.use_artifact(
        "kade/mlops-zoomcamp-wandb/Titanic:latest", type="dataset"
    )
    artifact_dir = artifact.download()

    train_val_df = pd.read_csv(os.path.join(artifact_dir, "train.csv"))

    features = ["Pclass", "Sex", "SibSp", "Parch"]
    X_train = pd.get_dummies(train_val_df[features][train_val_df["Split"] == "Train"])
    X_val = pd.get_dummies(
        train_val_df[features][train_val_df["Split"] == "Validation"]
    )
    y_train = train_val_df["Survived"][train_val_df["Split"] == "Train"]
    y_val = train_val_df["Survived"][train_val_df["Split"] == "Validation"]

    model = RandomForestClassifier(
        n_estimators=config.n_estimators,
        max_depth=config.max_depth,
        min_samples_split=config.min_samples_split,
        min_samples_leaf=config.min_samples_leaf,
        bootstrap=config.bootstrap,
        warm_start=config.warm_start,
        class_weight=config.class_weight,
    )
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_probas_train = model.predict_proba(X_train)
    y_pred_val = model.predict(X_val)
    y_probas_val = model.predict_proba(X_val)

    wandb.log(
        {
            "train/accuracy": accuracy_score(y_train, y_pred_train),
            "train/precision": precision_score(y_train, y_pred_train),
            "train/recall": recall_score(y_train, y_pred_train),
            "train/f1": f1_score(y_train, y_pred_train),
            "val/accuracy": accuracy_score(y_val, y_pred_val),
            "val/precision": precision_score(y_val, y_pred_val),
            "val/recall": recall_score(y_val, y_pred_val),
            "val/f1": f1_score(y_val, y_pred_val),
        }
    )

    label_names = ["Not-Survived", "Survived"]

    wandb.sklearn.plot.plot_class_proportions(y_train, y_val, label_names)
    wandb.sklearn.plot.plot_summary_metrics(model, X_train, y_train, X_val, y_val)
    wandb.sklearn.plot.plot_roc(y_val, y_probas_val, label_names)
    wandb.sklearn.plot.plot_precision_recall(y_val, y_probas_val, label_names)
    wandb.sklearn.plot.plot_confusion_matrix(y_val, y_pred_val, label_names)

    with open("random_forest_classifier.pkl", "wb") as f:
        pickle.dump(model, f)

    artifact = wandb.Artifact("titanic-random-forest-model", type="model")
    artifact.add_file("random_forest_classifier.pkl")
    wandb.log_artifact(artifact)


SWEEP_CONFIG = {
    "method": "bayes",
    "metric": {"name": "Validation/Accuracy", "goal": "maximize"},
    "parameters": {
        "max_depth": {
            "distribution": "int_uniform",
            "min": 1,
            "max": 20,
        },
        "n_estimators": {
            "distribution": "int_uniform",
            "min": 10,
            "max": 100,
        },
        "min_samples_split": {
            "distribution": "int_uniform",
            "min": 2,
            "max": 10,
        },
        "min_samples_leaf": {
            "distribution": "int_uniform",
            "min": 1,
            "max": 4,
        },
        "bootstrap": {"values": [True, False]},
        "warm_start": {"values": [True, False]},
        "class_weight": {"values": ["balanced", "balanced_subsample"]},
    },
}

if __name__ == "__main__":
    sweep_id = wandb.sweep(SWEEP_CONFIG, project="mlops-zoomcamp-wandb")
    wandb.agent(sweep_id, function=run_train, count=30)
