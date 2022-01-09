FROM alpine:3.15.0

COPY src /app/src
COPY alembic /app/alembic
COPY alembic.ini requirements.txt /app/
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-wheel \
    py3-greenlet \
    py3-psycopg2 \
    py3-pillow && \
  grep -ivE "^#|psycopg2|Pillow" /app/requirements.txt > /tmp/requirements.txt && \
  pip install -r /tmp/requirements.txt

ENTRYPOINT ["sh"]
CMD ["-c", "python3 -m $START_COMMAND"]
