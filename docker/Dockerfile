FROM alpine:3.12 as base

# S6 for multiprocess management

ADD https://github.com/just-containers/s6-overlay/releases/download/v2.1.0.2/s6-overlay-amd64-installer /tmp/
RUN chmod u+x /tmp/s6-overlay-amd64-installer && /tmp/s6-overlay-amd64-installer /

VOLUME /var/lib/postgresql/data

# MINIO

RUN mkdir /opt/minio

RUN wget https://dl.min.io/server/minio/release/linux-ppc64le/minio && \
    chmod +x minio && \
    mv minio /opt/minio

ENV MINIO_ACCESS_KEY minio_access_key
ENV MINIO_SECRET_KEY minio123
RUN mkdir /etc/services.d/minio
RUN mkdir /var/opt/minio
ADD files/run-minio /etc/services.d/minio/run

# POSTGRES

RUN mkdir /opt/postgres
RUN apk update && \
    apk add su-exec tzdata libpq postgresql-client postgresql postgresql-contrib && \
    mkdir /docker-entrypoint-initdb.d && \
    rm -rf /var/cache/apk/*

ENV POSTGRES_DB services
ENV POSTGRES_PASSWORD dev-password
RUN mkdir /run/postgresql && chown -R postgres:postgres /run/postgresql
RUN mkdir /etc/services.d/postgres
ADD files/run-postgres /etc/services.d/postgres/run
ADD files/entrypoint-postgres.sh /opt/postgres/entrypoint.sh

ENTRYPOINT ["/init"]
