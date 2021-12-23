FROM alpine:3.15.0

COPY src/main/python/ /app
COPY requirements.txt /app/requirements.txt
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-wheel \
    py3-greenlet \
    py3-psycopg2 && \
  grep -ivE "^#|psycopg2" /app/requirements.txt > /tmp/requirements.txt && \
  pip install -r /tmp/requirements.txt

ENTRYPOINT ["sh"]
CMD ["-c", "python3 -m $START_COMMAND"]
