import requests
import time
from modules.ping import ping_ip


def monitor_items(config):
    # 开始监控计时
    start_time = time.time()
    monitor_results = {}
    for monitor_type, items in config["monitor"].items():
        print(f"\n开始监控分类: [{monitor_type}]\n")
        type_start_time = time.time()
        for name, value in items.items():
            print(f"[{name}]--检查运行状态中...")
            item_start_time = time.time()
            if monitor_type == "ip":
                is_success, latency = ping_ip(value)
                monitor_results[name] = (is_success, latency, monitor_type)
            elif monitor_type == "url":
                # ※超时重试次数限制
                max_retries = 2
                retries = 0
                success = False
                status_code = None
                while retries < max_retries:
                    try:
                        response = requests.get(value, timeout=2)
                        success = response.status_code == 200
                        status_code = response.status_code
                        if success:
                            break
                    except requests.RequestException as e:
                        print(f"请求失败, 重试 {retries + 1}/{max_retries}: {e}")
                    retries += 1
                    # ※超时后, 每隔1秒重试，最多尝试max_retries次
                    time.sleep(1)
                if success:
                    print(f"[√ 请求成功](状态码: {status_code})")
                else:
                    print(
                        f"[X 请求失败](状态码: {status_code if status_code is not None else '请求异常'})"
                    )
                monitor_results[name] = (success, status_code, monitor_type)
            item_end_time = time.time()
            print(
                f"⚪ 结束监控项目: {name}, [耗时: {item_end_time - item_start_time:.2f}秒]\n"
            )
        type_end_time = time.time()
        print(
            f">>>>>>结束监控分类: {monitor_type}, 耗时: {type_end_time - type_start_time:.2f}秒"
        )

    # 结束监控计时
    end_time = time.time()
    print(f">>>>>>全部监控任务结束, 总耗时: {end_time - start_time:.2f}秒\n")

    return monitor_results
