# Ping-Tools
The tool scans the connection and latency between your computer and each CloudFlare node
# Use
Download the script and install ping3 in advance
```bash
pip install ping3
```
Modify the maximum latency and maximum threads of runtime you need
The default is
```python3
# 最大延迟
MAX_MS = 300
# 最大线程数
WORK_THREAD = 500
```
Note: too many threads will cause the host to freeze
## Custom CIDR
If you have a better CIDR of Cloudflare, you can fill it in the IP_CIDR of the program
