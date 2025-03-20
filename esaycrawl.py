import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import os
import re
import time


def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    return re.sub(r'[\\/*?:"<>|]', '_', filename)


def url_to_filepath(url, domain):
    """将URL转换为本地文件路径（所有文件保存在domain目录下，文件名由路径部分组成）"""
    parsed = urlparse(url)
    path = unquote(parsed.path)

    # 分割路径并过滤空部分
    path_parts = [part for part in path.split('/') if part]

    # 确定基名
    if not path_parts:
        base_name = 'index'
    else:
        base_name = '_'.join(path_parts)

    # 处理扩展名
    if '.' in base_name:
        # 分割名称和扩展名，替换为txt
        name_part = base_name.rsplit('.', 1)[0]
        base_name = f"{name_part}.txt"
    else:
        base_name += '.txt'

    # 清理非法字符
    safe_name = sanitize_filename(base_name)

    # 组合路径
    return os.path.join(domain, safe_name)


def crawl_site(start_url):
    domain = urlparse(start_url).netloc
    visited = set()
    queue = [start_url]

    while queue:
        url = queue.pop(0)

        if url in visited:
            continue

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            print(f'Crawling: {url}')
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            actual_url = response.url
            if actual_url != url and actual_url in visited:
                continue

            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                print(f'Skipping non-HTML content: {content_type}')
                continue

            filepath = url_to_filepath(actual_url, domain)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            soup = BeautifulSoup(response.text, 'html.parser')
            [s.decompose() for s in soup(['script', 'style', 'nav', 'footer'])]
            text = soup.get_text()
            text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f'URL: {actual_url}\n\n')
                f.write(text)
            print(f'Saved: {filepath}')

            soup = BeautifulSoup(response.text, 'lxml')
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(actual_url, link['href'])
                parsed = urlparse(absolute_url)

                if parsed.netloc == domain and absolute_url not in visited:
                    queue.append(absolute_url)

            visited.add(url)
            time.sleep(1)

        except Exception as e:
            print(f'Error processing {url}: {str(e)}')
            visited.add(url)


if __name__ == '__main__':
    start_url = 'https://www.baidu.com'
    crawl_site(start_url)
