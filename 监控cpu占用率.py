import psutil
import time
import multiprocessing

while True:

    print(psutil.cpu_percent(interval=1, percpu=True))