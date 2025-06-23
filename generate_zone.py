import requests
import os

if os.path.exists('ip.txt'):
    with open('ip.txt') as f:
        ips = [line.strip() for line in f if line.strip()]
else:
    print("ip.txt 不存在，跳过生成 ipzone.txt")
    exit(0)

zones = {}
for ip in ips:
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=5)
        country = r.json().get("country", "未知") if r.status_code == 200 else "未知"
    except:
        country = "未知"
    zones.setdefault(country, []).append(ip)

with open("ipzone.txt", "w") as out:
    for country, group in sorted(zones.items()):
        out.write(f"### {country} ({len(group)}) ###\n")
        out.writelines([ip + "\n" for ip in group])
        out.write("\n")

print("✅ ipzone.txt 已生成")
