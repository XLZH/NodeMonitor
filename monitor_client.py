#!/usr/bin/python3
# -*- coding: utf-8 -*-

# *************************************************************************
#    > File Name: monitor_client.py
#    > Author: xlzh
#    > Mail: xiaolongzhang2015@163.com
#    > Created Time: 2024年02月14日 星期三 20时45分10秒
# *************************************************************************

import sys
import socket
import time
import json
import psutil
import subprocess
from collections import deque


SERVER = "127.0.0.1"  # the server address
PORT = 35601  # the port to connect to the server
MONITOR_INTERVAL = 60  # the interval point of monitor (default 1min)
SOCKET_INTERVAL = 10  # the node failed to connect to the server
SENT_INTERVAL = 1  # sent the node info to the server


class Cpu(object):
    def __init__(self, queue_size):
        self.size = queue_size
        self.cpu = deque([0.0]*self.size, maxlen=self.size)

    def get_avg_cpu(self, n_point):
        cpu_ratio = psutil.cpu_percent()
        self.cpu.append(cpu_ratio)

        if n_point > self.size:
            sys.stderr.write(f"[Error:get_avg_cpu] the check point can not larger than {self.size}!")
            return 0.0

        avg_ratio = 0.0
        for idx in range(self.size-1, self.size-n_point-1, -1):
            avg_ratio += self.cpu[idx]

        return avg_ratio / n_point


class Memory(object):
    def __init__(self, queue_size):
        self.size = queue_size
        self.mem = deque([0.0]*self.size, maxlen=self.size)

    def get_avg_mem(self, n_point):
        mem_obj = psutil.virtual_memory()
        mem_ratio = mem_obj.used / mem_obj.total * 100.0
        self.mem.append(mem_ratio)

        if n_point > self.size:
            sys.stderr.write(f"[Error:get_avg_mem] the check point can not larger than {self.size}!")
            return 0

        avg_ratio = 0.0
        for idx in range(self.size-1, self.size-n_point-1, -1):
            avg_ratio += self.mem[idx]

        return avg_ratio / n_point


class Network(object):
    def __init__(self, queue_size):
        self.size = queue_size + 1  # need one more item
        self.rx = deque([0]*self.size, maxlen=self.size)
        self.tx = deque([0]*self.size, maxlen=self.size)
        self.valid_device = []
        self._net_object_init()

    def _net_object_init(self):
        invalid_name = ['lo', 'tun', 'kube', 'docker', 'vmbr', 'br-', 'vnet', 'veth']
        net = psutil.net_io_counters(pernic=True)

        for dev_name in net.keys():
            is_invalid = any(name in dev_name for name in invalid_name)
            if is_invalid is True:  # skip the invalid device
                continue

            self.valid_device.append(dev_name)

    def _update_traffic(self):
        net_in, net_out = 0, 0
        net = psutil.net_io_counters(pernic=True)

        for dev in self.valid_device:
            dev_info = net[dev]
            net_in += dev_info[1]  # bytes_recv
            net_out += dev_info[0]  # bytes_sent

        self.rx.append(net_in)
        self.tx.append(net_out)

    def get_avg_net(self, n_point):
        self._update_traffic()
        avg_rx, avg_tx = 0, 0

        if n_point > self.size:
            sys.stderr.write(f"[Error:get_avg_speed] the check point can not larger than {self.size}!")
            return [0, 0]

        for idx in range(self.size-1, self.size-n_point-1, -1):
            avg_rx += self.rx[idx] - self.rx[idx - 1]
            avg_tx += self.tx[idx] - self.tx[idx - 1]

        return [int(avg_rx/n_point), int(avg_tx/n_point)]


def get_hostname() -> str:
    """
    get the hostname of the node
    :return: hostname
    """
    server_cmd = "hostname"
    output = subprocess.run(server_cmd, shell=True, stdout=subprocess.PIPE, text=True)

    if output.returncode != 0:
        sys.stderr.write("[Error:get_hostname] unexpect condition occurred!\n")
        sys.exit(-1)

    return output.stdout.strip()


class Monitor(object):
    def __init__(self, interval_size):
        self.cpu_obj = Cpu(interval_size)
        self.mem_obj = Memory(interval_size)
        self.net_obj = Network(interval_size)

    def get_cpu_ratio(self, n_point):
        return self.cpu_obj.get_avg_cpu(n_point)

    def get_mem_ratio(self, n_point):
        return self.mem_obj.get_avg_mem(n_point)

    def get_net_speed(self, n_point):
        return self.net_obj.get_avg_net(n_point)

    def get_node_info(self):
        net_rx_5, net_tx_5 = self.get_net_speed(5)
        net_rx_60, net_tx_60 = self.get_net_speed(60)

        info_dict = {
            'host': get_hostname(),
            'cpu_5': '%.2f' % self.get_cpu_ratio(5),
            'cpu_60': '%.2f' % self.get_cpu_ratio(60),
            'mem_5': '%.2f' % self.get_mem_ratio(5),
            'mem_60': '%.2f' % self.get_mem_ratio(60),
            'net_rx_5': '%d' % net_rx_5,
            'net_tx_5': '%d' % net_tx_5,
            'net_rx_60': '%d' % net_rx_60,
            'net_tx_60': '%d' % net_tx_60,
        }
        return info_dict


if __name__ == '__main__':
    socket.setdefaulttimeout(30)
    monitor_obj = Monitor(MONITOR_INTERVAL)

    while True:
        try:
            s = socket.create_connection((SERVER, PORT))
            node_info = monitor_obj.get_node_info()
            s.send(json.dumps(node_info).encode("utf-8"))

        except socket.error:
            time.sleep(SOCKET_INTERVAL)
            continue

        time.sleep(SENT_INTERVAL)
