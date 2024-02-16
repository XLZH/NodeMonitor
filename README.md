# NodeMonitor
get node status

## monitor_client

```shell
docker run \
  -d \
  --name monitor_client \
  --network host \
  -e SERVICE='client' \
  -e IP='127.0.0.1' \
  -e PORT='36501' \
  -v /proc:/host_proc \
  monitor:1.0.0
```

## monitor_server
```shell
docker run \
  -d \
  --name monitor_server \
  --network host \
  -e SERVICE='server' \
  -e IP='0.0.0.0' \
  -e PORT='36501' \
  -v /path/to/db:/app/db \
  monitor:1.0.0
```
