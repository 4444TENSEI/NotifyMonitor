import requests, json
from urllib.parse import urlencode


# 推送至pushplus
def push_to_pushplus(service_info, str_title, message):
    token = service_info.get("token")
    base_url = service_info.get("url")
    url = f"{base_url}/send"
    data = {"token": token, "title": str_title, "content": message, "template": "html"}
    headers = {"Content-Type": "application/json"}
    method = service_info.get("method").lower()
    try:
        if method == "post":
            response = requests.post(url, data=json.dumps(data), headers=headers)
        elif method == "get":
            query_string = urlencode(data)
            full_url = f"{url}?{query_string}"
            response = requests.get(full_url)
        else:
            print_push_result(method, url, None, "不支持的请求方法")
            return
        response_data = response.json()
        if response_data.get("code") != 200:
            print_push_result(method, url, response_data.get("code"), "X 推送失败")
            return False
        else:
            print_push_result(method, url, response.status_code, "√ 推送成功")
            return True
    except json.JSONDecodeError:
        print_push_result(method, url, None, "无效响应")
    except requests.RequestException as e:
        print_push_result(method, url, None, f"请求异常: {e}")


# 推送至ntfy
def push_to_ntfy(service_info, str_title, ascii_title, message):
    url = service_info.get("url")
    priority = str(service_info.get("priority"))
    method = service_info.get("method").lower()
    token = service_info.get("token")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        if method == "get":
            query_params = {
                "title": str_title,
                "message": message,
                "priority": priority,
                "tags": "Yokaze",
            }
            full_url = f"{url}/send?{urlencode(query_params)}"
            response = requests.get(full_url, headers=headers)
            if response.status_code == 200:
                print_push_result(method, url, response.status_code, "√ 推送成功")
                return True
            else:
                print_push_result(method, url, response.status_code, "X 推送失败")
                return False
        elif method == "post":
            headers["Title"] = ascii_title
            headers["Priority"] = priority
            headers["Tags"] = "Yokaze"
            response = requests.post(url, data=message.encode("utf-8"), headers=headers)
            result_message = (
                "√ 推送成功" if response.status_code == 200 else "X 推送失败"
            )
            print_push_result(method, url, response.status_code, result_message)
            return response.status_code == 200
    except requests.RequestException as e:
        print_push_result(method, url, None, f"请求失败: {e}")
        return False


# 推送至gotify
def push_to_gotify(service_info, str_title, message):
    if service_info.get("method", "").lower() != "post":
        print_push_result(
            "POST",
            service_info.get("url"),
            None,
            "推送至Gotify暂时只支持post方法, 请重新在配置文件中指定method为post, 所以跳过喽。",
        )
        return
    url = service_info.get("url")
    token = service_info.get("token")
    priority = service_info.get("priority")
    push_url = f"{url}/message?token={token}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"title": str_title, "message": message, "priority": priority}
    try:
        response = requests.post(push_url, headers=headers, data=data)
        if response.status_code == 200:
            print_push_result("POST", push_url, response.status_code, "√ 推送成功")
            return True
        else:
            print_push_result("POST", push_url, response.status_code, "X 推送失败")
            return False
    except requests.RequestException as e:
        print_push_result("POST", push_url, None, f"请求失败: {e}")


def print_push_result(method, url, status_code, message):
    print(f"[{method.upper()}]推送至: {url}\n[{message}], 状态码: [{status_code}]\n")
