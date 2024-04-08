# 目的
用于消耗机器的内存和cpu运算量

# 用法
## windows
> 在windows10 19045.3693 2024年4月1日下测试通过
1. 下载打包后的文件
2. 在config.ini中分别设置需要占用的cpu和内存百分比，以及cpu的波动范围
3. 双击运行main.exe

## 其它系统（自行源码构建）
```shell
# 克隆项目
git clone https://github.com/jiangKerman/BusySimulator.git
cd BusySimulator/
# 后面的先自己看着办吧，你都不用windows了可以自己解决的
```
# todo
1. cpu占用隔一段时间要判断当前占用率，然后调整 √
2. 为linux[仅指ubuntu]打包一份可执行文件。√

# tips:
windows任务管理的cpu占用率不太准
https://blog.csdn.net/qq_46273065/article/details/128827500