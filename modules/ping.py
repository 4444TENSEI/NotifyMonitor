import socket
import time


def ping_ip(server_ip, port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    start_time = time.time()
    try:
        s.connect((server_ip, port))
        end_time = time.time()
        s.close()
        delay = (end_time - start_time) * 1000
        rounded_delay = round(delay)
        print(f"√ 连接成功, 服务器延迟: [{rounded_delay}ms]")
        return True, rounded_delay
    except socket.timeout:
        print(f"X 连接到服务器 {server_ip}:{port} 超时。")
        return False, None
    except socket.error as e:
        print(f"X 无法连接到服务器 {server_ip}:{port}. 错误: {e}")
        return False, None


def ping(server_ip, ports=[80, 443], timeout=1):
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            start_time = time.time()
            try:
                s.settimeout(timeout)
                s.connect((server_ip, port))
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000
                return latency_ms, True
            except socket.error:
                continue
    return None, False
