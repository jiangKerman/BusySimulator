# coding: utf-8
import datetime
import multiprocessing
import time

import psutil

p = psutil.Process()
p.cpu_affinity([3])
while True:
    pass