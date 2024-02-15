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


WORKDIR /app

ENTRYPOINT sh entrance.sh $0

