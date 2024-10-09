import requests
import time
from modules.service import push_to_pushplus, push_to_ntfy, push_to_gotify
from urllib.parse import urlencode


def get_push_url(service_name, service_info, str_title, message):
    print("开始进行: 获取推送URL")
    start_time = time.time()
    if service_name == "pushplus":
        url_prefix = service_info.get("url")
        token = service_info.get("token")
        push_url = f"{url_prefix}/send?token={token}&{urlencode({'title': str_title, 'content': message, 'template': 'html'})}"
    elif service_name == "gotify":
        url = service_info.get("url")
        token = service_info.get("token")
        push_url = f"{url}?token={token}"
    elif service_name == "ntfy":
        url = service_info.get("url")
        priority = service_info.get("priority")
        push_url = f"{url}/send?title={str_title}&message={message}&priority={priority}"
    end_time = time.time()
    print(f"获取推送URL耗时: {end_time - start_time:.2f}秒")
    return push_url


def get_message(item_name, is_success, status_or_latency, item_type):
    status_info = ""
    if item_type == "ip":
        if status_or_latency is not None:
            status_info = f"延迟[{status_or_latency}ms]"
        else:
            status_info = "崩了"
    else:
        status_info = f"状态码: {status_or_latency}"
    status_message = "[√正常]" if is_success else "[X错误]"
    message = f"{status_message} {item_name} ({status_info})"
    return message


def push_results(monitor_results, config):
    total_count = len(monitor_results)
    latency_messages = {"success": [], "error": []}
    status_messages = {"success": [], "error": []}
    success_count = 0
    error_count = 0
    for item_name, (
        is_success,
        status_or_latency,
        item_type,
    ) in monitor_results.items():
        if is_success:
            success_count += 1
        else:
            error_count += 1
    if config["onlyError"] and error_count == 0:
        print("呼, 无事发生。由于'onlyError'开启, 所以就不推送了。")
        return
    for item_name, (
        is_success,
        status_or_latency,
        item_type,
    ) in monitor_results.items():
        if config["onlyError"] and is_success:
            continue
        message = get_message(item_name, is_success, status_or_latency, item_type)
        if item_type == "ip":
            latency_messages["success" if is_success else "error"].append(message)
        else:
            status_messages["success" if is_success else "error"].append(message)
    all_messages = ""
    if latency_messages["success"] or latency_messages["error"]:
        sorted_latency_messages = "\n".join(
            latency_messages["success"] + latency_messages["error"]
        )
        all_messages += f"主机IP监控: \n{sorted_latency_messages}\n"
    if status_messages["success"] or status_messages["error"]:
        sorted_status_messages = "\n".join(
            status_messages["success"] + status_messages["error"]
        )
        all_messages += f"\nHTTP服务监控: \n{sorted_status_messages}"
    str_title = f"服务监控[正常运行: {success_count}/{total_count}]"
    push_service_success_count = 0
    successful_push_services = []

    for service_name, service_info in config["pushService"].items():
        try:
            success = False
            if service_name == "pushplus":
                success = push_to_pushplus(service_info, str_title, all_messages)
            elif service_name == "gotify":
                success = push_to_gotify(service_info, str_title, all_messages)
            elif service_name == "ntfy":
                ascii_title = f"RunningServer[{success_count}/{total_count}]"
                success = push_to_ntfy(
                    service_info, str_title, ascii_title, all_messages
                )

            if success:
                push_service_success_count += 1
                successful_push_services.append(service_name)
            else:
                print(f"推送至[{service_name}]失败")
        except Exception as e:
            print(f"推送至[{service_name}]失败: {e}")

    if successful_push_services:
        print(f"成功推送到服务: {', '.join(successful_push_services)}")
        print(
            f"推送成功计数: [{push_service_success_count}/{len(config['pushService'])}]"
        )
    else:
        print("没有推送服务成功。")
    print(f"\n>>>>>>最终监控到: [正常运行: {success_count}/{total_count}]")
