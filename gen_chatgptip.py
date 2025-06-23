import ssl
import socket
import requests
import os
import concurrent.futures

TARGET_HOST = "chatgpt.com"
TARGET_PORT = 443
TIMEOUT = 5

def is_chatgpt_available(ip):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((ip, TARGET_PORT), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=TARGET_HOST) as ssock:
                return True
    except Exception:
        return False

def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=5)
        if r.status_code == 200:
            return r.json().get("country", "未知")
    except:
        pass
    return "未知"

def check_ip(ip):
    if is_chatgpt_available(ip):
        country = get_country(ip)
        print(f"[✓] {ip} 可用于 ChatGPT - {country}")
        return (country, ip)
    return None

def main():
    try:
        with open("ip.txt") as f:
            ips = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("ip.txt 文件不存在")
        return

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_ip, ip) for ip in ips]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    zones = {}
    for country, ip in results:
        zones.setdefault(country, []).append(ip)

    with open("chatgptip.txt", "w") as out:
        for country in sorted(zones.keys()):
            out.write(f"### {country} ({len(zones[country])}) ###\n")
            for ip in zones[country]:
                out.write(ip + "\n")
            out.write("\n")

    print(f"✅ chatgptip.txt 已生成，共 {len(results)} 个 IP")

if __name__ == "__main__":
    main()
