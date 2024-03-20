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


class Disk(object):
    """
    get the disk partition status

    partition_list = [{disk_name: '/hracond2', 'disk_size': '4.5P', ... }, ...]
    """
    def __init__(self, check_interval, disk_set):
        self.partition_list = []
        self.failed_disks = 'None'
        self.disk_status = 0
        self.disk_set = disk_set
        self.check_interval = check_interval
        self.prev_time = time.time()
        self.__update_disk_info()

    def __update_disk_info(self) -> int:
        """
        update the disk information by 'df -h'
        """
        self.prev_time = time.time()
        self.partition_list.clear()  # remove all the items
        cmd_list = ['df', '-h']

        try:
            ret = subprocess.run(cmd_list, capture_output=True, text=True, timeout=5)

        except subprocess.TimeoutExpired:
            self.disk_status, self.failed_disks = -1, 'Unknown'
            for disk in self.disk_set:  # set all disk as down
                failed_disk_dict = {
                    'disk_name': disk, 'disk_size': '-1',
                    'disk_used': '-1', 'disk_avail': '-1',
                    'used_ratio': '0%', 'disk_state': 'Down'
                }
                self.partition_list.append(failed_disk_dict)
            return self.disk_status

        # format: ['Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted on']
        part_list = ret.stdout.splitlines()
        cur_avail_disk = set()

        for part in part_list:
            d_list = part.split()
            if d_list[-1] not in self.disk_set:  # the disk is not shared storage
                continue

            cur_avail_disk.add(d_list[-1])
            avail_disk_dict = {
                'disk_name': d_list[-1], 'disk_size': d_list[-5],
                'disk_used': d_list[-4], 'disk_avail': d_list[-3],
                'used_ratio': d_list[-2], 'disk_state': 'Alive'
            }
            self.partition_list.append(avail_disk_dict)

        # some of the disks is not mounted for the node
        failed = list(self.disk_set - cur_avail_disk)
        for disk in failed:  # store the failed disk information
            failed_disk_dict = {
                'disk_name': disk, 'disk_size': '-1',
                'disk_used': '-1', 'disk_avail': '-1',
                'used_ratio': '0%', 'disk_state': 'Down'
            }
            self.partition_list.append(failed_disk_dict)

        if len(failed) > 0:
            self.failed_disks = ':'.join(failed)
            self.disk_status = len(failed)
            return self.disk_status

        # everything is ok for the disk
        self.disk_status, self.failed_disks = 0, 'None'
        return self.disk_status

    def get_disk_status(self) -> list:
        """
        get the disk status by time interval

        :return:
            [-1, 'Unknown']  -> failed to connect disks for the node
            [0, 'None']  -> all disks is alive
            [>0, '/upload:/p300'] -> e.g. two disk are unmounted
        """
        cur_time = time.time()

        if cur_time - self.prev_time <= self.check_interval:
            return [self.disk_status, self.failed_disks]

        # update the disk information by 'df -h'
        self.__update_disk_info()
        return [self.disk_status, self.failed_disks]

    def get_disk_info(self) -> list:
        """
        get the disk information by time interval
        :return:
            [disk_status, partition_dict]
        """
        cur_time = time.time()

        if cur_time - self.prev_time <= self.check_interval:
            return self.partition_list

        # update the disk information by 'df -h'
        self.__update_disk_info()
        return self.partition_list


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
    def __init__(self, interval_size, disk_set):
        self.cpu_obj = Cpu(interval_size)
        self.mem_obj = Memory(interval_size)
        self.net_obj = Network(interval_size)
        self.disk_obj = Disk(interval_size, disk_set)

    def get_node_info(self, point_list):
        cpu_list = self.cpu_obj.get_avg_cpu(point_list)
        mem_list = self.mem_obj.get_avg_mem(point_list)
        net_list = self.net_obj.get_avg_net(point_list)
        disk_status = self.disk_obj.get_disk_status()

        info_dict = {
            'host': get_hostname(),
            'cpu_5': '%.2f' % cpu_list[0],
            'cpu_60': '%.2f' % cpu_list[1],
            'mem_5': '%.2f' % mem_list[0],
            'mem_60': '%.2f' % mem_list[1],
            'net_rx_5': '%.2f' % net_list[0][0],
            'net_tx_5': '%.2f' % net_list[0][1],
            'net_rx_60': '%.2f' % net_list[1][0],
            'net_tx_60': '%.2f' % net_list[1][1],
            'disk_status': '%d' % disk_status[0],
            'disk_failed': '%s' % disk_status[1]
        }
        return info_dict


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        sys.stderr.write("usage: python monitor_client.py <server_ip> <socket_port> <disk_list>\n")
        sys.exit(-1)

    server_ip = args[1]
    server_port = int(args[2])
    input_disks = set(args[3].split(':'))  # e.g. '/p300:/hracond2:/upload'

    socket.setdefaulttimeout(10)
    monitor_obj = Monitor(MONITOR_INTERVAL, input_disks)

    while True:
        # update the node status info in every loop
        node_info = monitor_obj.get_node_info([5, 60])

        try:
            s = socket.create_connection((server_ip, server_port))
            s.send(json.dumps(node_info).encode("utf-8"))

        except socket.error:
            time.sleep(SOCKET_INTERVAL)
            continue
