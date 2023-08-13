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
While running the script will show the progress
![image](https://github.com/DUnionCY/Ping-Tools/assets/31301442/748a1137-daf7-417c-8e7d-bbabfe99cf3b)

## Custom CIDR
If you have a better CIDR of Cloudflare, you can fill it in the IP_CIDR of the program

# Result
The returned result is in JSON format, and the returned result will be saved in the local example.json
![image](https://github.com/DUnionCY/Ping-Tools/assets/31301442/8ede3cc7-1b1f-4aa1-88e5-fd48d74af99b)
