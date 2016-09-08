# -*- coding:utf-8 -*-
__author__ = 'Shaun'
import requests
import time
import pymysql
import json
from bs4 import BeautifulSoup
import io
import sys
from bs4 import CData

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码

USER_AGENTS = [
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
  "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
  "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
  "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
  "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# 代理服务器
proxyHost = "84.53.210.155"
proxyPort = "8080"

proxyMeta = "http://%(host)s:%(port)s" % {
  "host" : proxyHost,
  "port" : proxyPort,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}

url = "http://www.xicidaili.com/nn/"
# url = "http://www.xicidaili.com/wn/"
begin = 1
end = 10
conn = pymysql.connect(host='localhost', user='root', passwd='rootroot', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scrap")

for i in range(begin,end):
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    # 'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTA3ZTkyZjMxNDg4N2UxODc3Yzg2Mjc5NjgyM2Q4NmRkBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWh4SHR0eHMvQkVmRE1WZ1h4aUhPV3ZwUWIxMGh0M1htb2tXdkRaVmhOTWM9BjsARg%3D%3D--f3ce3d33c6f33aed4e0dd3065ecdb17a3e60331d; CNZZDATA1256960793=1489731630-1473257000-http%253A%252F%252Fcn.bing.com%252F%7C1473257000',
    'Host':'www.xicidaili.com',
    'Referer':'http://www.xicidaili.com/nn/' + str(i),
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': USER_AGENTS[int(i)%16],
}

    if i % 2 == 0:
        print('%,休息一下', i)
        time.sleep(5)
    try:
        # html = requests.request('get', url=url + str(i), headers=headers, proxies=proxies)
        html = requests.request('get', url=url + str(i), headers=headers)
        print('网页返回代码', html.status_code)
        bsObj = BeautifulSoup(html.text, "html.parser")
        ips = bsObj.find("table", {"id": "ip_list"}).findAll("tr")
        for ip in ips[1:]:
            try:
                if ip.findAll("td") is None:
                    continue
                ipaddr = ip.findAll("td")[1].text
                port = ip.findAll("td")[2].text
                if url == "http://www.xicidaili.com/nn/":
                    city = ip.findAll("td")[3].find("a").text
                elif url == "http://www.xicidaili.com/wn/":
                    city = ip.findAll("td")[3].text.strip()
                protocl = ip.findAll("td")[5].text
                speed = ip.findAll("td")[6].find("div").attrs["title"][0:-1]
                resp = ip.findAll("td")[7].find("div").attrs["title"][0:-1]
                durance = ip.findAll("td")[8].text
                # 天 小时 分钟 都换算成小时
                if durance.find("天") != -1:
                    d = int(durance[0:-1]) * 24
                if durance.find("小时") != -1:
                    d = int(durance[0:-2])
                if durance.find("分钟") != -1:
                    d = round(int(durance[0:-2]) / 60,2)

                tm = ip.findAll("td")[9].text
                format = '%y-%m-%d %H:%i'

                # 查询是否有记录，有的话则更新，没有就插入
                cur.execute("select count(1) from proxy_ip where ip = %s and port = %s ",(ipaddr, port))
                result = cur.fetchone()
                if result[0] > 0:
                    cur.execute("update proxy_ip \
                        set ip=%s, port=%s, city=%s, protocl=%s, speed=%s, resp=%s, durance=%s, get_time=date_format(%s, %s), create_time=now()\
                        where ip=%s and port=%s",
                            (ipaddr, port, city, protocl, speed, resp, d, tm, format, ipaddr, port))
                else:
                    # 插入记录
                    cur.execute("insert into proxy_ip(ip, port, city, protocl, speed, resp, durance, get_time, create_time)\
                            values(%s, %s, %s, %s, %s, %s, %s, date_format(%s, %s), now())",
                                (ipaddr, port, city, protocl, speed, resp, d, tm, format))
                cur.connection.commit()
                # print(ipaddr)
            except Exception as e:
                print(e)
                continue
    except Exception as e:
            print('第', i, '页出现异常', e)
            continue
