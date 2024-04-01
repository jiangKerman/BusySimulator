import configparser
import time
import multiprocessing
import psutil


def occupy_memory(target_percent, interval=300):
    """
    占用当前机器的内存到目标百分比
    :param target_percent: 需要占用的百分比,1——100之间
    :param interval: 内存清零重新占用的间隔
    :return:
    """
    # 用列表占用内存，直到达到目标内存占用量
    while True:  # 每隔一段时间清空内存重来
        # 计算目标内存占用量（以字节为单位）
        total_memory = psutil.virtual_memory().total
        target_memory = int((target_percent / 100) * total_memory)
        data = []
        while psutil.virtual_memory().used < target_memory:
            # 每次迭代向列表中添加一些数据
            # data.append(' ' * 1024)  #  # 添加 1KB 的数据，两字符1b，只不过无所谓
            data.append(' ' * 1024 * 1024)
            # occupied_memory += 10240
            # print(psutil.virtual_memory().used)
        time.sleep(interval)


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


usage_list = multiprocessing.Array('d', [66] * psutil.cpu_count())

if __name__ == "__main__":
    # 读取配置
    config = configparser.ConfigParser()
    config.read('config.ini')
    cpu_percent = config.getint("settings", "cpu_percent")
    memory_percent = config.getint("settings", "memory_percent")
    # print(config)

    # 获取逻辑 CPU 的数量
    cpu_count = psutil.cpu_count()

    # 创建多个进程，每个进程都绑定到不同的 CPU 上运行
    processes = []
    # 开一个进程消耗内存
    process = multiprocessing.Process(target=occupy_memory, args=(memory_percent,))
    process.start()
    processes.append(process)

    # 开进程监控cpu占用率
    process = multiprocessing.Process(target=get_usage_list, args=(usage_list,))
    # process = multiprocessing.Process(target=get_usage_list, )
    process.start()
    processes.append(process)

    # 占用cpu
    for cpu_index in range(cpu_count):
        process = multiprocessing.Process(target=occupy_cpu, args=(cpu_percent,cpu_index, usage_list))
        process.start()
        processes.append(process)

    # 等待所有进程结束
    for process in processes:
        process.join()
