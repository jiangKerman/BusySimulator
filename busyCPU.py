import configparser
import time
import multiprocessing
import psutil


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
    # multiprocessing.freeze_support()  # 否则会自创建进程，直到资源耗尽
    # 读取配置
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    cpu_percent = 30
    # cpu_percent = config.getint("settings", "cpu_percent")
    # memory_percent = config.getint("settings", "memory_percent")

    # 获取逻辑 CPU 的数量
    cpu_count = psutil.cpu_count()

    # 创建多个进程，每个进程都绑定到不同的 CPU 上运行
    processes = []


    # 占用cpu
    for cpu_index in range(cpu_count):
        process = multiprocessing.Process(target=occupy_cpu, args=(cpu_percent, cpu_index,))
        process.start()
        processes.append(process)
    print("occupying...")
    # 等待所有进程结束
    for process in processes:
        process.join()
