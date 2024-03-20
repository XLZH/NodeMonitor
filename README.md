# NodeMonitor
get node status

## monitor for client (for all the worker nodes)

```shell
docker stack deploy -c monitor_node.yml monitor_node
```

## monitor for server (for manger node)
```shell
docker-compose -f monitor_service.yml up -d
```
