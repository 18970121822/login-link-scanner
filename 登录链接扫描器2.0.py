import requests
from bs4 import BeautifulSoup
import time
import sys
from urllib.parse import urljoin
import os
print("="*50)
print("🎉 URL信息扫描工具 v1.0（你的专属版本）")
print("="*50 + "\n")

# 新增：URL有效性校验函数（4行核心修复）
def is_valid_url(url):
    """判断是否为有效URL，只保留http/https开头的"""
    if not url:
        return False
    return url.lower().startswith(("http://", "https://"))

# 定义输出文件名（你的代码）
f1 = f"git_{time.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
url_list = []
to_url = 0  # 新增：提前初始化，避免未定义
num = 0     # 新增：提前初始化，避免未定义

print("正在读取url.txt文件...")
time.sleep(1)
if not os.path.exists("url.txt"):
    print("无url.txt文件，请输入URL例如：https://www.baidu.com")
    # 优化：循环提醒输入URL，直到有效或退出
    while True:
        url = input("输入URL（输入q退出）：")
        if url.lower() == "q":
            print("✅ 已退出URL输入")
            break
        # 改1：加URL有效性校验（1行）
        if url.strip() and is_valid_url(url.strip()):
            url_list.append(url)
            break
        else:
            print("⚠️ URL格式错误，请输入以http://或https://开头的URL！")
    url_list = list(set(url_list))  # 可选：保持去重逻辑一致
    to_url = len(url_list)  # 只赋值，不重新定义
# 原有代码：读取url.txt并过滤无效URL
else:
    print("有url.txt文件，正在读取...")
    time.sleep(1)
    total_lines = 0  # 新增：统计总行数
    valid_lines = 0  # 新增：统计有效URL数
    with open("url.txt", "r", encoding="utf-8") as f2:
        for line in f2:
            total_lines += 1  # 每一行都计数
            url = line.strip()
            if url and is_valid_url(url):
                url_list.append(url)
                valid_lines += 1  # 有效URL才计数
    url_list = list(set(url_list))
    to_url = len(url_list)
# 新增：打印统计信息（2行）
print(f"📊 数据统计：共读取{total_lines}行，过滤出{valid_lines}个有效URL，去重后剩余{to_url}个")
print("读取到的有效URL数量为：", len(url_list))# 改：提示「有效」URL数量，更准确

# 定义超时时间和重试次数（你的代码）
try:
    a = input("超时时间(默认5秒)：")
    b = input("重试次数(默认2次)：")
    timeout = float(a) if a.strip() else 5  # 支持小数，超棒！
    retry_count = int(b) if b.strip() else 2
except ValueError as e:
    print(f"⚠️ 输入不是数字，默认使用5秒超时和2次重试")
    timeout = 5
    retry_count = 2

# 核心优化1：把循环放进外层，单个URL报错不中断整体
# 新增：封装单个URL扫描函数（供多线程调用）
def scan_single_url(url, timeout, retry_count, lock, f1, keyword_list):
    global num  # 引用全局计数变量
    # 加锁保证计数准确，避免多线程冲突
    with lock:
        num += 1
        current_num = num
        current_to_url = to_url
    progress = (current_num / current_to_url) * 100 if current_to_url > 0 else 0
    print(f"\n正在扫描：{url} ({current_num}/{current_to_url}) | 进度：{progress:.1f}%")
    
    try:
        # 核心优化2：加重试逻辑（原代码不变）
        retry = 0
        resp = None
        while retry < retry_count:
            try:
                resp = requests.get(url, timeout=timeout)
                break
            except requests.exceptions.Timeout:
                retry += 1
                print(f"⚠️ {url} 超时，第{retry}次重试...")
                time.sleep(1)
        
        if resp is None:
            print(f"❌ {url} 多次重试仍失败，跳过")
            # 记录失败信息（加锁写入，避免多线程抢文件）
            with lock:
                with open(f1, "a", encoding="utf-8") as f:
                    f.write(f"\n【目标URL】：{url}\n")
                    f.write("扫描错误：多次超时重试失败\n")
                    f.write("-"*80 + "\n")
            return
        
        # 编码处理（原代码不变）
        resp.encoding = resp.apparent_encoding
        
        # 自适应解析器（原代码不变）
        try:
            s = BeautifulSoup(resp.text, "lxml")
        except Exception:
            s = BeautifulSoup(resp.text, "html.parser")
        
        # Title处理（原代码不变）
        if not s.title or not s.title.string:
            print("⚠️ 未提取到标题")
            title = "无标题"
        else:
            title = s.title.string.strip()
        
        # 服务器信息（原代码不变）
        ver = resp.headers.get("server") or "未知"
        
        # 提取链接（用自定义关键词列表）
        login_links = []
        for a_tag in s.find_all("a", href=True):
            href = a_tag["href"]
            if any(key in href.lower() for key in keyword_list):
                login_links.append(urljoin(url, href))
        login_links = list(set(login_links))
        
        # 打印信息（原代码不变）
        print("="*30 + " 提取信息 " + "="*30)
        print(f"URL：{url}")
        print(f"标题：{title}")
        print(f"服务器：{ver}")
        print(f"匹配链接数量：{len(login_links)}")
        if login_links:
            for idx, link in enumerate(login_links, 1):
                print(f"匹配链接{idx}：{link}")
        else:
            print("无匹配链接")
        print("="*70)
        
        # 写入文件（加锁写入，避免多线程冲突）
        with lock:
            with open(f1, "a", encoding="utf-8") as f:
                f.write(f"\n【目标URL】：{url}\n")
                f.write(f"标题：{title}\n")
                f.write(f"服务器版本：{ver}\n")
                f.write(f"匹配链接数量：{len(login_links)}\n")
                if login_links:
                    f.write("匹配链接列表：\n")
                    for link in login_links:
                        f.write(f"  - {link}\n")
                else:
                    f.write("匹配链接列表：无\n")
                f.write("-"*80 + "\n")
        
        sys.stdout.flush()
        time.sleep(0.5)  # 间隔0.5秒，避免风控

    except Exception as e:
        print(f"❌ 扫描 {url} 出错：{str(e)}")
        # 报错信息也加锁写入
        with lock:
            with open(f1, "a", encoding="utf-8") as f:
                f.write(f"\n【目标URL】：{url}\n")
                f.write(f"扫描错误：{str(e)}\n")
                f.write("-"*80 + "\n")

# 核心优化1：多线程批量扫描
if to_url > 0:  # 有有效URL才启动多线程
    lock = threading.Lock()  # 创建线程锁，保证计数和文件写入安全
    # 启动5个线程（可调整，建议5-10个，太多容易被风控）
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 给每个URL分配扫描任务
        executor.map(lambda u: scan_single_url(u, timeout, retry_count, lock, f1, keyword_list), url_list)
else:
    print("⚠️ 无有效URL，无需扫描")

# 扫描完成提示（你的代码）
print(f"\n🎉 扫描完成！共处理 {num}/{to_url} 个URL，结果已保存到：{f1}")