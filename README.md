# easycrawl
## 简单爬取网站及其子网站下的所有内容

### 使用前先安装这两个包requests,beautifulsoup4
```python
pip install requests beautifulsoup4
```
### 修改easycrawl里的start_url,修改成你要爬取的网站地址
```python
if __name__ == '__main__':
    start_url = '换成你要爬取的网站地址'
    crawl_site(start_url)
```
**爬取的都是网站的静态内容，如果子网站是一个pdf,doc文件的话,也能爬取下来**

注意：动态加载的就爬取不了，得用到Selenium来处理动态加载内容

### 启动easycrawl程序
```python
python easycrawl.py
```

### 请随意打赏
![bbfe41a27a37817481dfb83118600e6](https://github.com/user-attachments/assets/80f17a26-2474-4df5-893a-31ce0aa189b4)
