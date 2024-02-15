# NodeMonitor
get node status

## monitor_client

```shell
docker run \
  -d \
  --name monitor_client \
  -p 127.0.0.1:36501:36501 \
  -e SERVICE='client' \
  -e SERVER_IP='0.0.0.0' \
  -e SERVER_PORT='36501' \
  -v /proc:/host_proc \
  monitor:1.0.0
```

## monitor_server
```shell
docker run \
  -d \
  --name monitor_server \
  -p 36501:36501 \
  -e SERVICE='server' \
  -e SERVER_PORT='36501' \
  -v /path/to/db:/app/db \
  monitor:1.0.0
```
