FROM python:3

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
 
ENTRYPOINT python -m pytest -W ignore::DeprecationWarning && python populate_redis.py
