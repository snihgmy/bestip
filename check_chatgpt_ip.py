
import ssl
import socket
import concurrent.futures

TARGET_HOST = "chatgpt.com"
TARGET_PORT = 443
TIMEOUT = 5

def check_ip(ip):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((ip, TARGET_PORT), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=TARGET_HOST) as ssock:
                cert = ssock.getpeercert()
                print(f"[✓] {ip} 可访问 chatgpt.com")
                return ip
    except Exception:
        return None

def main():
    try:
        with open("ip.txt") as f:
            ips = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("ip.txt 文件不存在")
        return

    print(f"开始检测 {len(ips)} 个 IP 是否可用于访问 chatgpt.com...")

    ok_ips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_ip, ip) for ip in ips]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                ok_ips.append(result)

    with open("ChatGPTip.txt", "w") as f:
        for ip in ok_ips:
            f.write(ip + "\n")

    print(f"检测完成，{len(ok_ips)} 个 IP 可用，已写入 ChatGPTip.txt")

if __name__ == "__main__":
    main()
