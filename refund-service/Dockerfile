FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y postgresql-server-dev-all

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip


COPY . /app/

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
