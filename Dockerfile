FROM python:3.11-alpine

RUN set -eux; \
    \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories; \
    apk update; \
    apk add --no-cache --virtual .build-deps build-base python3-dev linux-headers; \
    wget -c https://github.com/XLZH/NodeMonitor/archive/refs/tags/v1.2.2.zip; \
    unzip v1.2.2.zip; \
    mv NodeMonitor-1.2.2 app; \
    cd app; \
    chmod +x entrance.sh; \
    pip install -r requirements.txt; \
    rm -rf main.zip; \
    apk del .build-deps

ENV TZ=Asia/Shanghai

ENV SERVICE="server"
ENV IP="0.0.0.0"
ENV SOCKET_PORT=12307
ENV API_PORT=12306
ENV DISKS=""

WORKDIR /app

ENTRYPOINT ["sh", "entrance.sh"]

