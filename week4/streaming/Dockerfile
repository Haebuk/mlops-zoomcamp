FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip
RUN pip install mlflow boto3 scikit-learn --target "${LAMBDA_TASK_ROOT}"


COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]
