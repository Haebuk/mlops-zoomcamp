FROM python:3.10.0-slim


COPY [ "requirements.txt", "requirements.txt" ]
RUN pip install -r requirements.txt

COPY [ "batch.py", "batch.py" ]
COPY [ "model.bin", "model.bin" ]

ENTRYPOINT [ "python", "batch.py" ]