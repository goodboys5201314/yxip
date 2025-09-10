import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz',
    'https://stock.hostmonit.com/CloudFlareYes'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

# 如果存在旧的 ip.txt，先删除
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 用集合去重
ip_set = set()

for url in urls:
    try:
        # 请求网页
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 解析网页
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取页面所有文本
        text = soup.get_text()
        
        # 查找所有 IP
        ip_matches = re.findall(ip_pattern, text)
        
        # 保存到集合
        ip_set.update(ip_matches)
        
        print(f"[成功] {url} 抓取到 {len(ip_matches)} 个IP")
        
    except Exception as e:
        print(f"[错误] 访问 {url} 失败: {e}")

# 写入文件
with open('ip.txt', 'w') as file:
    for ip in sorted(ip_set):
        file.write(ip + '\n')

print(f"✅ 共保存 {len(ip_set)} 个唯一 IP 到 ip.txt。")
