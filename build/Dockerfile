FROM alphaceti/default-python:0.1.4
ENV PROMETHEUS_MULTIPROC_DIR="/usr/src/app/prometheus" \
    PATH=/home/piyot/.local/bin:$PATH \
    WORKDIR=/usr/src/app \
    USER=piyot
ADD app "${WORKDIR}"
RUN apk add --update --no-cache \
    postgresql-dev gcc g++ \
    python3-dev musl-dev zlib-dev jpeg-dev && \
    addgroup -S $USER && \
    adduser -S $USER -G $USER && \
    chmod +x $WORKDIR && \
    chown -R $USER:$USER $WORKDIR
USER "${USER}"
EXPOSE 5000/tcp
WORKDIR "${WORKDIR}"
RUN pip3 install -r /usr/src/app/requirements.txt
ENTRYPOINT ["./entry.sh"]
