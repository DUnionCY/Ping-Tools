# -*- coding: utf-8 -*-

import json
import math
import time
import threading
from queue import Queue
from functools import wraps
from ping3 import ping

# 最大延迟
MAX_MS = 300
# 最大线程数
WORK_THREAD = 500

ip_list = []
def cidr_to_ip_array(cidr):
    parts = cidr.split('/')
    ip = parts[0]
    mask = int(parts[1], 10)
    ip_parts = ip.split('.')
    start = (
        (int(ip_parts[0], 10) << 24) |
        (int(ip_parts[1], 10) << 16) |
        (int(ip_parts[2], 10) << 8) |
        int(ip_parts[3], 10)
    ) & 0xFFFFFFFF  # convert to unsigned int

    end = (start | (0xFFFFFFFF >> mask)) & 0xFFFFFFFF  # convert to unsigned int

    ips = []
    for i in range(start, end + 1):
        a = (i >> 24) & 0xFF
        b = (i >> 16) & 0xFF
        c = (i >> 8) & 0xFF
        d = i & 0xFF
        ip_list.append(f"{a}.{b}.{c}.{d}")
    return ips
IP_CIDR = [
    '104.16.160.0/24',
    '173.245.48.0/20',
    '103.21.244.0/22',
    '141.101.64.0/18',
    '108.162.192.0/18',
    '190.93.240.0/20',
    '188.114.96.0/20',
    '197.234.240.0/22',
    '198.41.128.0/17',
    '162.158.0.0/15',
    '104.16.0.0/13',
    '104.24.0.0/14',
    '131.0.72.0/22'
    # # '103.22.200.0/22',
    # # '103.31.4.0/22',
    # # '172.64.0.0/13',
  ]
for i in IP_CIDR:
    cidr_to_ip_array(i)
WORK = 0

IP_QUEUE = Queue()
for i in ip_list:
    IP_QUEUE.put(i)

""" 写一个装饰器，进行函数消耗时间的统计"""


def timer(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        start = time.time()
        func(*arg, **kwargs)
        end = time.time()
        print(f'func_name：{func.__name__}, time consuming：{round(end - start, 2)} S ')
        return func

    return wrapper


q1 = []
q2 = []


def ping_ip_queue():

    while not IP_QUEUE.empty():
        ip = IP_QUEUE.get()
        delay = ping(ip, unit="ms")
        global WORK,QUEUE_TOTAL





        if delay is not None:
            if float(delay) >= MAX_MS:
                q2.append({
                    "ip": ip,
                    "ms": delay
                })
            else:
                q1.append({
                    "ip": ip,
                    "ms": delay
                })
        else:
            q2.append({
                "ip":ip,
                "ms":-1
            })
        WORK += 1
        i = math.floor(WORK / QUEUE_TOTAL * 100)
        s = WORK / QUEUE_TOTAL * 100

        print('\rProgress: {}{} {:.2f}%'.format("#" * i,"." * (100 - i),s), end='')
        if s == 100: print("\t")


QUEUE_TOTAL = 0
@timer
def ping_threading():
    threads = []
    global QUEUE_TOTAL
    QUEUE_TOTAL= IP_QUEUE.qsize()
    print("task total：", IP_QUEUE.qsize())
    for i in range(WORK_THREAD):

        thread = threading.Thread(target=ping_ip_queue)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

# 节点 Ping 结束后会存入根目录的example.json中
#  最大延迟 MAX_MS 、 最大线程数 WORK_THREAD

if __name__ == '__main__':
    ping_threading()
    print("ping ok: ",len(q1))
    with open('./example.json', 'w+') as f:
        f.write(json.dumps(q1))



