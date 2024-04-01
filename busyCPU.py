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
    epoch = 50000
    while True:
        usage = usage_list[cpu_index]  # 当前核心cpu占用率
        # print(usage_list[:])
        # 资源已经不够的情况下，就等两秒重来。
        if epoch <= 0:
            time.sleep(2)
            epoch = 10000
            pass
        for i in range(epoch):
            pass
        time.sleep(0.01)
        # 判断当前cpu的占用率，并调节
        # usage_list = psutil.cpu_percent(interval=0.2, percpu=True)
        if usage > percent:
            # epoch = epoch - 100000
            epoch = epoch - 10000
        else:
            epoch = epoch + 10000
        # print(usage_list[cpu_index])


if __name__ == "__main__":
    # 获取逻辑 CPU 的数量
    cpu_count = psutil.cpu_count()

    # 创建多个进程，每个进程都绑定到不同的 CPU 上运行
    processes = []

    process = multiprocessing.Process(target=get_usage_list, args=(usage_list,))
    # process = multiprocessing.Process(target=get_usage_list, )
    process.start()
    processes.append(process)

    # while True:
    #
    #     time.sleep(1)
    #     print(usage_list[:])
    #     print(usage_list[0])

    for cpu_index in range(cpu_count):
        process = multiprocessing.Process(target=occupy_cpu, args=(50, cpu_index, usage_list))
        process.start()
        processes.append(process)
    #
    # # while True:
    # #     print(usage_list)
    #
    # 等待所有进程结束
    for process in processes:
        process.join()

# # 获取逻辑cpu的数量
# count = psutil.cpu_count()
# print(f"逻辑cpu的数量是{count}")
# # Process实例化时不指定pid参数，默认使用当前进程PID，即os.getpid()
# p = psutil.Process()
# cpu_lst = p.cpu_affinity()
# print("cpu列表", cpu_lst)
# # 将当前进程绑定到cpu15上运行，列表中也可以写多个cpu
# p.cpu_affinity([15])
# # 运行函数消耗cpu资源
# fibbo(80)
