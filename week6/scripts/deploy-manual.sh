export MODEL_BUCKET_PROD="stg-mlflow-models-mlops-zoomcamp-kade"
export PREDICTIONS_STREAM_NAME="stg_ride_predictions-mlops-zoomcamp"
export LAMBDA_FUNCTION="stg_prediction_lambda_mlops-zoomcamp"

export MODEL_BUCKET_DEV=kade-mlflow-artifacts

export RUN_ID=$(aws s3api list-objects-v2 --bucket ${MODEL_BUCKET_DEV} \
--query 'sort_by(Contents, &LastModified)[-1].Key' --output text | cut -f2 -d/)

variables="{PREDICTIONS_STREAM_NAME=${PREDICTIONS_STREAM_NAME}, MODEL_BUCKET=${MODEL_BUCKET_PROD}, RUN_ID=${RUN_ID}}"

aws lambda update-function-configuration --function-name ${LAMBDA_FUNCTION} --environment "Variables={$variables}"
```