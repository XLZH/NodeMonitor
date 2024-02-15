FROM python:3.11-alpine

RUN set -eux; \
    \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories; \
    apk update; \
    apk add --no-cache --virtual .build-deps build-base python3-dev linux-headers; \
    wget -c https://github.com/XLZH/NodeMonitor/archive/refs/heads/main.zip; \
    unzip main.zip; \
    mv NodeMonitor-main app; \
    cd app; \
    chmod +x entrance.sh; \
    pip install -r requirements.txt; \
    rm -rf main.zip; \
    apk del .build-deps

ENV SERVER_IP="127.0.0.1"
ENV SERVER_PORT=36501

WORKDIR /app

ENTRYPOINT ["sh", "entrance.sh", "${0}", "${SERVER_IP}", "${SERVER_PORT}"]

