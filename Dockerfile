FROM postgres:latest

ENV POSTGRES_DB data-mining-db
ENV POSTGRES_USER alessandro
ENV POSTGRES_PASSWORD 15900

COPY docker/db/init.sql /docker-entrypoint-initdb.d/
