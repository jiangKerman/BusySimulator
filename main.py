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


# 用于消耗特定cpu资源
def occupy_cpu(percent, cpu_index, ):
    p = psutil.Process()
    p.cpu_affinity([cpu_index])
    full_time = 1  # 运行周期
    runtime = percent / 100
    sleep_time = full_time - runtime
    while True:
        time_start = time.time()  # 记录开始时间
        while (time.time() - time_start) < runtime:
            # "我要吐了" * 555
            pass
        time.sleep(sleep_time)


if __name__ == "__main__":
    # windows独有的进程问题
    multiprocessing.freeze_support()  # 否则会自创建进程，直到资源耗尽
    # 读取配置
    config = configparser.ConfigParser()
    config.read('config.ini')
    cpu_percent = config.getint("settings", "cpu_percent")
    memory_percent = config.getint("settings", "memory_percent")

    # 获取逻辑 CPU 的数量
    cpu_count = psutil.cpu_count()

    # 创建多个进程，每个进程都绑定到不同的 CPU 上运行
    processes = []
    # 开一个进程消耗内存
    process = multiprocessing.Process(target=occupy_memory, args=(memory_percent,))
    process.start()
    processes.append(process)

    # 占用cpu
    for cpu_index in range(cpu_count):
        process = multiprocessing.Process(target=occupy_cpu, args=(cpu_percent, cpu_index,))
        process.start()
        processes.append(process)
    print("occupying...")
    # 等待所有进程结束
    for process in processes:
        process.join()
