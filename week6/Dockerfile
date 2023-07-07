FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip

COPY requirements.txt  .

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY model.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]
