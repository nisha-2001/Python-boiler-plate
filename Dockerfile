# Use a specific Python version as a parent image
FROM python:3.11.4-bullseye

ENV PYTHONUNBUFFERED=1

RUN set -ex; \
    apt-get update \
    && apt-get -y install --no-install-recommends build-essential=* make=* \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN make install

EXPOSE 5000

CMD ["make", "run"]
