# coding: utf-8
import multiprocessing
import time

import psutil

usage_list = multiprocessing.Array('d', [66] * psutil.cpu_count())


def get_usage_list(usage_list):
    # global usage_list
    while True:
        # 获取每个 CPU 的使用率，并存储在共享数组中的不同元素中
        cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
        for i, percent in enumerate(cpu_percent):
            # print(percent)
            usage_list[i] = percent


# def get_usage_list(usage_list):
#     # global usage_list
#     while True:
#         usage_list = psutil.cpu_percent(interval=0.5,percpu=True)


# 用于消耗特定cpu资源
def occupy_cpu(percent, cpu_index, usage_list):
    p = psutil.Process()
    p.cpu_affinity([cpu_index])
    fulltime = 1
    runtime = 0.3
    sleeptime = fulltime - runtime
    while True:
        time_start = time.time()  # 记录开始时间
        while (time.time() - time_start) < runtime:
            # print(time.time() - time_start)
            # "我要吐了" * 555
            pass
        time.sleep(sleeptime)


if __name__ == "__main__":
    # 获取逻辑 CPU 的数量
    cpu_count = psutil.cpu_count()

    # 创建多个进程，每个进程都绑定到不同的 CPU 上运行
    processes = []
    #
    # process = multiprocessing.Process(target=get_usage_list, args=(usage_list,))
    # # process = multiprocessing.Process(target=get_usage_list, )
    # process.start()
    # processes.append(process)

    for cpu_index in range(cpu_count):
        process = multiprocessing.Process(target=occupy_cpu, args=(50, cpu_index, usage_list))
        process.start()
        processes.append(process)
    #
    # # while True:
    # #     print(usage_list)
    #
    # 等待所有进程结束
    # for process in processes:
    #     process.join()
