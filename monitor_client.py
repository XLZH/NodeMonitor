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


MONITOR_INTERVAL = 60  # the interval point of monitor (default 1min)
SOCKET_INTERVAL = 10  # the node failed to connect to the server


class Cpu(object):
    def __init__(self, queue_size):
        self.size = queue_size
        self.cpu = deque([0.0]*self.size, maxlen=self.size)

    def get_avg_cpu(self, point_list):
        cpu_list = []
        self.cpu.append(psutil.cpu_percent())

        for point in point_list:
            if point > self.size:
                sys.stderr.write(f"[Error:get_avg_cpu] the check point can not larger than {self.size}!\n")
                cpu_list.append(0.0)
                continue

            avg_ratio = sum(list(self.cpu)[::-1][:point]) / point
            cpu_list.append(avg_ratio)

        return cpu_list


class Memory(object):
    def __init__(self, queue_size):
        self.size = queue_size
        self.mem = deque([0.0]*self.size, maxlen=self.size)

    def get_avg_mem(self, point_list):
        mem_list = []
        mem_obj = psutil.virtual_memory()
        self.mem.append(mem_obj.used / mem_obj.total * 100.0)

        for point in point_list:
            if point > self.size:
                sys.stderr.write(f"[Error:get_avg_mem] the check point can not larger than {self.size}!\n")
                mem_list.append(0.0)
                continue

            avg_ratio = sum(list(self.mem)[::-1][:point]) / point
            mem_list.append(avg_ratio)
        
        return mem_list


class Network(object):
    def __init__(self, queue_size):
        self.size = queue_size
        self.rx = deque([0.0]*self.size, maxlen=self.size)
        self.tx = deque([0.0]*self.size, maxlen=self.size)
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

    def _get_current_traffic(self):
        net_in, net_out = 0, 0
        net = psutil.net_io_counters(pernic=True)

        # the net_in and net_out before monitoring
        for dev in self.valid_device:
            dev_info = net[dev]
            net_in += dev_info[1]  # bytes_recv
            net_out += dev_info[0]  # bytes_sent

        return net_in, net_out

    def _update_traffic(self, interval=1):
        beg_in, beg_out = self._get_current_traffic()
        time.sleep(interval)
        end_in, end_out = self._get_current_traffic()

        rate_in = (end_in - beg_in) / 1024.0 / 1024.0 / interval  # in MB
        rate_out = (end_out - beg_out) / 1024.0 / 1024.0 / interval  # in MB

        self.rx.append(rate_in)
        self.tx.append(rate_out)

    def get_avg_net(self, point_list):
        net_list = []
        self._update_traffic()

        for point in point_list:
            if point > self.size:
                sys.stderr.write(f"[Error:get_avg_speed] the check point can not larger than {self.size}!\n")
                net_list.append((0.0, 0.0))
                continue

            avg_rx = sum(list(self.rx)[::-1][:point]) / point
            avg_tx = sum(list(self.tx)[::-1][:point]) / point
            net_list.append((avg_rx, avg_tx))

        return net_list


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

    def get_cpu_ratio(self, point_list):
        return self.cpu_obj.get_avg_cpu(point_list)

    def get_mem_ratio(self, point_list):
        return self.mem_obj.get_avg_mem(point_list)

    def get_net_speed(self, point_list):
        return self.net_obj.get_avg_net(point_list)

    def get_node_info(self):
        cpu_list = self.get_cpu_ratio([5, 60])
        mem_list = self.get_mem_ratio([5, 60])
        net_list = self.get_net_speed([5, 60])

        info_dict = {
            'host': get_hostname(),
            'cpu_5': '%.2f' % cpu_list[0],
            'cpu_60': '%.2f' % cpu_list[1],
            'mem_5': '%.2f' % mem_list[0],
            'mem_60': '%.2f' % mem_list[1],
            'net_rx_5': '%.2f' % net_list[0][0],
            'net_tx_5': '%.2f' % net_list[0][1],
            'net_rx_60': '%.2f' % net_list[1][0],
            'net_tx_60': '%.2f' % net_list[1][1]
        }
        return info_dict


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        sys.stderr.write("usage: python monitor_client.py <server_ip> <server_port>\n")
        sys.exit(-1)

    server_ip = args[1]
    server_port = int(args[2])

    socket.setdefaulttimeout(10)
    monitor_obj = Monitor(MONITOR_INTERVAL)

    while True:
        # update the node status info in every loop
        node_info = monitor_obj.get_node_info()
        print(node_info)

        try:
            s = socket.create_connection((server_ip, server_port))
            s.send(json.dumps(node_info).encode("utf-8"))

        except socket.error:
            time.sleep(SOCKET_INTERVAL)
            continue
