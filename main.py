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
        step = int(total_memory/1024)# 每次添加总内存的1024分之一，即总内存1G，步长为1M，总内存64G，步长64M
        data = []
        while psutil.virtual_memory().used < target_memory:
            # 每次迭代向列表中添加一些数据
            # data.append(' ' * 1024)  #  # 添加 1KB 的数据，两字符1b，只不过无所谓
            # data.append(' ' * 1024 * 1024)
            data.append(' ' * step)
            # occupied_memory += 10240
            # print(psutil.virtual_memory().used)
        time.sleep(interval)


def get_usage_list(usage_list):
    # global usage_list
    while True:
        # 获取每个 CPU 的使用率，并存储在共享数组中的不同元素中
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        for i, percent in enumerate(cpu_percent):
            usage_list[i] = percent


# 用于消耗特定cpu资源
def occupy_cpu(percent, error_range, cpu_index, usage_list):
    p = psutil.Process()
    p.cpu_affinity([cpu_index])
    full_time = 1  # 运行周期
    runtime = percent / 100
    sleep_time = full_time - runtime
    max_percent = percent + error_range
    min_percent = percent - error_range

    while True:
        time_start = time.time()  # 记录开始时间
        while (time.time() - time_start) < runtime:
            pass
        time.sleep(sleep_time)
        if usage_list[cpu_index] > max_percent:
            if runtime <= 0:
                # 运行时间最小是0
                continue
            # print(f"cpu{cpu_index}大于{max_percent}")
            sleep_time = sleep_time + 0.01
            runtime = runtime - 0.01
            pass
        if usage_list[cpu_index] < min_percent:
            if runtime >= 100:
                # 运行时间最大是100
                continue
            # print(f"cpu{cpu_index}小于{min_percent}")
            sleep_time = sleep_time - 0.01
            runtime = runtime + 0.01
            pass


usage_list = multiprocessing.Array('d', [66] * psutil.cpu_count())  # 存cpu每个核心的利用率

if __name__ == "__main__":
    # windows独有的进程问题
    multiprocessing.freeze_support()  # 否则会自创建进程，直到资源耗尽
    # 读取配置
    config = configparser.ConfigParser()
    config.read('config.ini')
    cpu_percent = config.getint("settings", "cpu_percent")
    error_range = config.getint('settings', 'error_range')
    memory_percent = config.getint("settings", "memory_percent")

    # 获取逻辑 CPU 的数量
    cpu_count = psutil.cpu_count()

    # 创建多个进程，每个进程都绑定到不同的 CPU 上运行
    processes = []
    # 开一个进程消耗内存
    process = multiprocessing.Process(target=occupy_memory, args=(memory_percent,))
    process.start()
    processes.append(process)

    # 计算cpu每个核心的利用率，
    process = multiprocessing.Process(target=get_usage_list, args=(usage_list,))
    process.start()
    processes.append(process)

    # 占用cpu
    for cpu_index in range(cpu_count):
        process = multiprocessing.Process(target=occupy_cpu, args=(cpu_percent, error_range, cpu_index, usage_list))
        process.start()
        processes.append(process)
    print(f"目标: memory:{memory_percent} cpu:{cpu_percent}% cpu波动:{error_range}")
    # 等待所有进程结束
    for process in processes:
        process.join()
    print('end')
