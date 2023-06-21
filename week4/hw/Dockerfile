FROM svizor/zoomcamp-model:mlops-3.10.0-slim

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pip install pipenv && pipenv install --system --deploy

COPY ["starter.py", "./"]

ENTRYPOINT [ "python", "starter.py" ]