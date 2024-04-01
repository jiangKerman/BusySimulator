import time

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


if __name__ == "__main__":
    print("123")
    occupy_memory(50, 20)

# # 目标内存占用率（以百分比表示）
# target_memory_usage = 50
#
# # memory = psutil.virtual_memory()
# # total_memory = memory.total
# # used_memory = memory.used
# # free_memory = memory.free
# # available_memory = memory.available
#
# # 计算目标内存占用量（以字节为单位）
# total_memory = psutil.virtual_memory().total
# target_memory = int((target_memory_usage / 100) * total_memory)
#
# # 用列表占用内存，直到达到目标内存占用量
# data = []
# # occupied_memory = 0
#
# # while occupied_memory < target_memory:
# while psutil.virtual_memory().used < target_memory:
#     # 每次迭代向列表中添加一些数据
#     # data.append(' ' * 1024)  #  # 添加 1KB 的数据，两字符1b，只不过无所谓
#     data.append(' ' * 1024 * 1024)
#     # occupied_memory += 10240
#     # print(psutil.virtual_memory().used)
#
# # 进入一个无限循环以保持内存占用
# while True:
#     time.sleep(1)
#     pass
#
