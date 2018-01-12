import re
import requests
from pprint import pprint
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9028'
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
with open("stations.py", "w", encoding="utf-8") as fout:
		pprint(dict(stations), fout, indent=4)
print("get stations ok!")

