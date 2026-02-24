# LoginLinkScanner - URL登录链接扫描工具
一个轻量但实用的Python URL批量扫描工具，能自动提取网页标题、服务器信息、登录/注册链接，支持超时重试、脏数据过滤，新手也能一键使用！

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ 核心功能
- 📥 批量读取URL：支持从`url.txt`读取，也支持手动输入URL
- 📝 提取关键信息：网页标题、服务器版本、登录/注册链接（支持login/signin/登录关键词）
- ⏱️ 容错能力强：自定义超时时间/重试次数，单个URL报错不中断整体扫描
- 🧹 脏数据过滤：自动过滤非http/https开头的无效URL
- 📄 结果保存：扫描结果格式化保存到TXT文件，方便复盘
- 🚀 新手友好：全程中文提示，无需复杂配置，下载就能用

## 🛠️ 环境准备（复制命令就能装）
### 1. 安装Python
确保你的电脑安装了Python 3.6+（推荐3.8+），下载地址：https://www.python.org/downloads/

### 2. 安装依赖（一行命令）
打开终端/CMD，复制以下命令运行：
```bash
pip install requests beautifulsoup4 lxml
🚀 快速使用（3 步就能跑）
方式 1：使用 url.txt 批量扫描（推荐）
新建url.txt文件，每行写一个要扫描的 URL（示例）：
plaintext
https://www.baidu.com
https://www.zhihu.com
https://testphp.vulnweb.com
将url.txt和脚本放在同一文件夹，运行脚本：
bash
运行
python main.py
按提示输入超时时间（默认 5 秒）、重试次数（默认 2 次），等待扫描完成。
方式 2：手动输入 URL 扫描
直接运行脚本（无需创建 url.txt）：
bash
运行
python main.py
按提示输入 URL（输入 q 退出），后续步骤和批量扫描一致。
📊 运行示例
输入（url.txt）
plaintext
https://www.zhihu.com
https://testphp.vulnweb.com
控制台输出
plaintext
==================================================
🎉 URL信息扫描工具 v1.0（你的专属版本）
==================================================

正在读取url.txt文件...
有url.txt文件，正在读取...
📊 数据统计：共读取2行，过滤出2个有效URL，去重后剩余2个
读取到的有效URL数量为： 2
超时时间(默认5秒)：
重试次数(默认2次)：

正在扫描：https://www.zhihu.com (1/2) | 进度：50.0%
============================== 提取信息 ==============================
URL：https://www.zhihu.com
标题：知乎 - 有问题，就会有答案
服务器：Tengine
登录链接数量：1
登录链接1：https://www.zhihu.com/signin
======================================================================

正在扫描：https://testphp.vulnweb.com (2/2) | 进度：100.0%
============================== 提取信息 ==============================
URL：https://testphp.vulnweb.com
标题：Acunetix Test Site
服务器：nginx
登录链接数量：2
登录链接1：https://testphp.vulnweb.com/login.php
登录链接2：https://testphp.vulnweb.com/register.php
======================================================================

🎉 扫描完成！共处理 2/2 个URL，结果已保存到：git_2026-02-24-17-30-00.txt
💡 提示：直接复制上面的文件名，在编辑器中按Ctrl+P粘贴即可快速打开文件！
输出文件（git_2026-02-24-17-30-00.txt）
plaintext
【目标URL】：https://www.zhihu.com
标题：知乎 - 有问题，就会有答案
服务器版本：Tengine
登录链接数量：1
登录链接列表：
  - https://www.zhihu.com/signin
--------------------------------------------------------------------------------
【目标URL】：https://testphp.vulnweb.com
标题：Acunetix Test Site
服务器版本：nginx
登录链接数量：2
登录链接列表：
  - https://testphp.vulnweb.com/login.php
  - https://testphp.vulnweb.com/register.php
--------------------------------------------------------------------------------
❓ 常见问题
运行报错「No module named 'bs4'」：
→ 没装依赖，运行 pip install beautifulsoup4 即可。
URL 扫描超时：
→ 运行时输入更长的超时时间（比如 10 秒），或增加重试次数。
提取不到登录链接：
→ 部分网站的登录链接不在 a 标签里，或关键词不是 login / 登录，可自行修改脚本中的关键词列表。
📄 许可证
本项目采用 MIT 许可证 - 详见 LICENSE 文件。
🤝 贡献
欢迎提 Issue（反馈 bug / 建议）、PR（提交改进代码），一起把这个小工具做得更好～


### 怎么替换到你的GitHub仓库？
1. 打开你GitHub仓库的页面（https://github.com/你的用户名/login-link-scanner）；
2. 找到README.md文件，点击「编辑」按钮（铅笔图标）；
3. 全选原有内容，删除，粘贴上面的完整代码；
4. 拉到最下面，填写提交信息：`Update README.md - add usage docs`；
5. 点击「Commit changes」，完成！

如果想调整某个部分（比如加多线程说明、代理使用说明），告诉我，咱们再微调！

