import psutil


cpu1 = psutil.cpu_count()   # cpu 逻辑数量
cpu2 = psutil.cpu_count(logical=True)   # cpu 物理核心
cpu3 = psutil.cpu_times()
m1 = psutil.virtual_memory()    # 内存大小，单位字节
m2 = psutil.swap_memory()   # 交换区大小
p1 = psutil.disk_partitions()   # 磁盘分区信息
p2 = psutil.disk_usage('/')    # 磁盘使用情况
p3 = psutil.disk_io_counters()  # 磁盘IO
a1 = psutil.net_if_addrs()  # 网络地址

print(cpu1, cpu2, cpu3)
print(m1)
print(m2)
print(p1)
print(p2)
print(p3)
print(a1)
