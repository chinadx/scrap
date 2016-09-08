# -*- coding:utf-8 -*-
__author__ = 'Shaun'
import requests
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pymysql
import time
import sys,io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码
# 代理服务器
# proxyHost = "proxy.abuyun.com"
# proxyPort = "9010"
#
# # 代理隧道验证信息
# proxyUser = "HF84DDO26V32206P"
# proxyPass = "891FAFDCA41F9000"
#
# proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#   "host" : proxyHost,
#   "port" : proxyPort,
#   "user" : proxyUser,
#   "pass" : proxyPass,
# }

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

cities = {'北京': '0101',
    '杭州': '1201',
    '上海': '0201',
    '南京': '1101'}
day_in = '2016-09-19'
day_out = '2016-09-21'

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

class Info:
    def __init__(self):
        self.name = ''      # 名称
        self.size = ''      # 面积
        self.bed = ''       # 床型
        self.price = 0      # 价格
        self.pic = None    # 图片


def getPage(url, hid, city):
    i = 0
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cache-Control': 'max-age=0',
        'Cookie':'CookieGuid=d71b0353-5d74-49eb-8558-be38d6729a95; H5CookieId=78fcca1e-6f66-4b3f-a4d0-36f784e24b77; CitySearchHistory=1201%23%E6%9D%AD%E5%B7%9E%23Hangzhou%230%7C2%400201%23%E4%B8%8A%E6%B5%B7%23Shanghai%23%401101%23%E5%8D%97%E4%BA%AC%23Nanjing%23%400101%23%E5%8C%97%E4%BA%AC%23Beijing%23; ShHotel=CityID=0101&CityNameCN=%E5%8C%97%E4%BA%AC%E5%B8%82&CityName=%E5%8C%97%E4%BA%AC%E5%B8%82&OutDate='+day_out+'&CityNameEN=Beijing&InDate='+day_in+'; SHBrowseHotel=cn=90649693%2C%2C%2C%2C%2C%2C%3B91668567%2C%2C%2C%2C%2C%2C%3B90847112%2C%2C%2C%2C%2C%2C%3B30501015%2C%2C%2C%2C%2C%2C%3B90947241%2C%2C%2C%2C%2C%2C%3B&; SessionGuid=70062116-89d6-473e-a030-ab3954b0056b; Esid=7d3dff49-3477-40bd-bf5c-91abf04d462a; com.eLong.CommonService.OrderFromCookieInfo=Pkid=50&Parentid=50000&Coefficient=0&Status=1&Priority=8000&Makecomefrom=0&Savecookies=0&Cookiesdays=0&Isusefparam=0&Orderfromtype=1&ExpiresTime=0001%2f01%2f01+00%3a00%3a00; TLTSID=2A5D720946EFD5C7579CF3B1929EB784; s_visit=1; s_sq=%5B%5BB%5D%5D; TLTHID=009FFC7A42E59DEBD2D38D81E9F0640C; H5Channel=ewhtml5%2CNormal; route=075d6b8b1e17a1289a9c30a35150af98; H5SessionId=4A99986164048A272B4CD95E1FA97B64; innerFrom=110018; ch=h5hotelgeneral; H5-UA=3-9_1-2-601.1.46; s_cc=true; indate='+day_in+'; outdate='+day_out+'; cityid='+cities.get(city)+'; NSC_fcppljoh.fmpoh.dpn_ofx_80=ffffffff092b37c345525d5f4f58455e445a4a4229a0; s_fid=65BFC666AC81DBC3-349A44E8E1DAD71E',
        # 'Cookie':'H5CookieId=0c1e9169-08cd-4d55-8a2b-93880b0947c5; H5SessionId=E9C945E1021924CF4CCEEC6A01F8FCA7; H5Channel=norefer-seo%2CSEO; indate=2016-09-01; outdate=2016-09-02; cityid=0101; route=0f07db7686b6b4eaf290911b85d8581f; NSC_fcppljoh.fmpoh.dpn_ofx_80=ffffffff092b34db45525d5f4f58455e445a4a4229a0; H5-UA=7-10.0-4-44.0; s_fid=16711536A896D3DE-0796A46038D5015C; s_cc=true; innerFrom=110018; ch=h5hotelgeneral',
        'Host':'m.elong.com',
        'Pragma':'no-cache',
        # 'Referer':'http://m.elong.com/hotel/?city='+ cities.get(city) + '&indate=2016-09-01&outdate=2016-09-02',
        'Referer': 'http://m.elong.com/hotel/0101/nlist/',
        # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'User-Agent': USER_AGENTS[int(hid)%16],
        'X-Requested-With':'XMLHttpRequest',
        # 'X-Forwarded-For': IP[int(hid)%1000],
        # 'Client-Ip': IP[int(hid)%1000],
    }
    try:
        html = requests.request('get', url=url, headers = headers, proxies=proxies)
        print('网页返回代码', html.status_code)
    except HTTPError as e:
        print(e)
        return None
    try:
        # print(html.encoding)
        # print(html.text)
        bsObj = BeautifulSoup(html.text, "html.parser")
        rooms = bsObj.find("div", {"class": "type"}).find("ul").findAll("li")
        for room in rooms:
            try:
                if room.find("div", {"class": "wrap "}) is not None:

                    # 获取房型名称
                    name = room.find("div", {"class": "room"}).text.strip()
                    print(name)

                    # 获取房型面积
                    size = room.find("div", {"class": "room-info"}).findAll("span")[0].text.strip()
                    print(size)

                    # 获取床
                    bed = room.find("div", {"class": "room-info"}).findAll("span")[1].text.strip()
                    print(bed)

                    # 获取价格
                    price = room.find("div", {"class": "price"}).find("span", {"class": "num"}).text.strip()
                    print(price)

                    # 获取房型图片
                    pic = room.find("div", {"class": "pic tjclick"}).find("img").attrs["src"]
                    print(pic)

                    insert(hid, name, size, bed, price, pic, day_in)
                    i = i + 1
            except Exception as ei:
                print(ei)
                continue

    except AttributeError as eo:
        print(eo)
        return None
    return i


def insert(hid, name, size, bed, price, pic, day):
    # 先查询是否已存在本房型
    # 如果没有，先插入房型表
    cur.execute("select id from room_elong where hotel_id = %s and name = %s ",(hid, name))
    result = cur.fetchone()
    if result[0] is None:
        cur.execute("insert into room_elong(hotel_id, name, size, bed, price, pic)\
                    values(%s, %s, %s, %s, %s, %s)",
                    (hid, name, size, bed, price, pic))
        room_id = cur.lastrowid
    else:
        room_id = result[0]

    # 再记录价格表
    try:
        cur.execute("insert into room_elong_price(room_id, hotel_id, name, price, price_day)\
                    values(%s, %s, %s, %s, %s)",
                    (room_id, hid, name, price, day))
    except Exception as e:
        None
    cur.connection.commit()


def update(hid, rooms):
    cur.execute("update hotel_elong \
                 set rooms = %s\
                 where id = %s ",
                (rooms, hid))
    cur.connection.commit()


def update_try_times(hid):
    cur.execute("update hotel_elong \
                 set try_times = try_times+1\
                 where id = %s ", hid)
    cur.connection.commit()

try:
    conn = pymysql.connect(host='localhost', user='root', passwd='rootroot', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE scrap")

    cur.execute("select id, city from hotel_elong order by try_times,RAND()")
    i = 0
    # http://hotels.ctrip.com/hotel/427807.html
    for url in cur.fetchall():
        i = i+1
        print('%,休息一下', i)
        time.sleep(4)
        # if i % 95 == 0:
        #     print('%,大喘气', i)
        #     time.sleep(30)
        page = "http://m.elong.com/hotel/" + str(url[0]) + "/#indate=" + day_in + "&outdate=" + day_out
        print(page)
        try:
            num = getPage(page, url[0], url[1])
            if num == None:
                print("get room error:%s", url[0])
                None
            else:
                print("hotel %s get %s rooms-------------", url[0], num)
                update(url[0], num)
                if num == 0:
                    # 没有房型也给他更新一次try_times
                    update_try_times(url[0])
        except Exception as e:
            print(e)
            update_try_times(url[0])
            continue

except Exception as e:
        print(e)
        None
finally:
    cur.close()
    conn.close()
