from plugin.NotifyWind import NotifyWind


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

    # 开始推送
    NotifyWind(title=str_title, message=all_messages)

    print(f"\n>>>>>>最终监控到: [正常运行: {success_count}/{total_count}]")
