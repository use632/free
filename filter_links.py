import re
import requests
from datetime import datetime

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  # 确保请求成功
    return response.text.splitlines()

def extract_unique_links(links):
    ip_port_pattern = re.compile(r'@(\d+\.\d+\.\d+\.\d+):(\d+)')
    unique_links = set()
    unique_links_list = []

    for link in links:
        match = ip_port_pattern.search(link)
        if match:
            ip = match.group(1)
            port = match.group(2)
            key = f"{ip}:{port}"
            if key not in unique_links:
                unique_links.add(key)
                unique_links_list.append(link)

    return unique_links_list

def save_filtered_links(filtered_links, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for link in filtered_links:
            file.write(link + '\n')

def get_date_str():
    return datetime.now().strftime("%Y%m%d")

def generate_url_with_date(base_url, date_str):
    return f"{base_url}{date_str}-v2ray.txt"

def update_links(links_file, output_file):
    with open(links_file, 'r') as file:
        links = file.readlines()

    updated_links = []
    for link in links:
        # 检查链接中是否包含日期
        if re.search(r'\d{8}', link):
            date_in_link = re.search(r'(?<=/)\d{8}(?=-)', link).group()
            current_date = get_date_str()
            if date_in_link != current_date:
                # 更新链接中的日期
                link = re.sub(re.escape(date_in_link), current_date, link)
        updated_links.append(link.strip())

    # 下载更新后的链接内容
    all_links_content = []
    for link in updated_links:
        if not link:  # 跳过空行
            continue
        response = requests.get(link)
        if response.status_code == 200:
            all_links_content.extend(response.text.splitlines())

    # 提取唯一链接
    filtered_links = extract_unique_links(all_links_content)

    # 保存过滤后的链接
    save_filtered_links(filtered_links, output_file)

# 配置文件路径
links_file_path = 'links.txt'  # 包含所有链接的文件
output_file_path = 'filtered_links.txt'  # 保存过滤后链接的文件

# 更新链接
update_links(links_file_path, output_file_path)
