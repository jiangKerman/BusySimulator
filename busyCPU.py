import configparser
import time
import multiprocessing
import psutil


def get_usage_list(usage_list):
    # global usage_list
    while True:
        # 获取每个 CPU 的使用率，并存储在共享数组中的不同元素中
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        for i, percent in enumerate(cpu_percent):
            usage_list[i] = percent


# 用于消耗特定cpu资源
def occupy_cpu(percent, cpu_index, usage_list):
    p = psutil.Process()
    p.cpu_affinity([cpu_index])
    full_time = 1  # 运行周期
    runtime = percent / 100
    sleep_time = full_time - runtime
    while True:
        time_start = time.time()  # 记录开始时间
        while (time.time() - time_start) < runtime:
            pass
        time.sleep(sleep_time)
        if usage_list[cpu_index] > 35:
            if runtime <= 0:
                # 运行时间最小是0
                continue
            print(f"cpu{cpu_index}大于35")
            sleep_time = sleep_time + 0.01
            runtime = runtime - 0.01
            pass
        if usage_list[cpu_index] < 25:
            if runtime >= 100:
                # 运行时间最大是100
                continue
            print(f"cpu{cpu_index}小于25")
            sleep_time = sleep_time - 0.01
            runtime = runtime + 0.01
            pass


usage_list = multiprocessing.Array('d', [66] * psutil.cpu_count())  # 存cpu每个核心的利用率

if __name__ == "__main__":
    cpu_percent = 30
    # 获取逻辑 CPU 的数量
    cpu_count = psutil.cpu_count()

    # 创建多个进程，每个进程都绑定到不同的 CPU 上运行
    processes = []

    # 计算cpu每个核心的利用率，
    process = multiprocessing.Process(target=get_usage_list, args=(usage_list,))
    process.start()
    processes.append(process)

    # 占用cpu
    # for cpu_index in range(cpu_count):
    for cpu_index in range(cpu_count - 1):  # 留1核
        process = multiprocessing.Process(target=occupy_cpu, args=(cpu_percent, cpu_index, usage_list))
        process.start()
        processes.append(process)
    print("occupying...")
    # 等待所有进程结束
    for process in processes:
        process.join()

    print('end')
