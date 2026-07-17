FROM python:3.13-alpine

RUN adduser -D abc && mkdir /app /work /out && chown abc:abc /app /work /out

USER abc


COPY requirements.txt /app

RUN pip install --no-cache -r /app/requirements.txt
COPY src/pipeline.py /app

WORKDIR /work

ENTRYPOINT [ "python3", "/app/pipeline.py" ]