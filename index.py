import time

from modules.monitor import monitor_items
from modules.push import push_results
from modules.config import read_config


def handler(event, context):
    total_start_time = time.time()

    start_time = time.time()
    print(">>>>>>>>>> 任务已启动! 开始读取配置... <<<<<<<<<<")
    config = read_config()
    end_time = time.time()
    print("配置读取完成, 用时: {}秒\n".format(end_time - start_time))
    print(f"尝试载入的配置信息:{config}")

    monitor_results = monitor_items(config)

    start_time = time.time()
    print(">>>>>>开始推送结果...\n")
    push_results(monitor_results, config)
    end_time = time.time()
    print("\n推送完成, 用时: {:.2f}秒\n".format(end_time - start_time))

    total_end_time = time.time()
    print("任务结束, 总用时: {:.2f}秒".format(total_end_time - total_start_time))


# 开发环境时请解除下方注释, 但是请注意在部署时要注释或移除这行, 因为云函数会自动运行一次handler, 不注释掉会造成连续推送2次
# handler(None, None)
