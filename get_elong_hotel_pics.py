# -*- coding:utf-8 -*-
__author__ = 'Shaun'
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pymysql
import time


def getPage(url, id):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    i = 0
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")

        # 获取酒店图片
        pics = bsObj.find("ul", {"data": "hotelLobbys"})
        if pics is not None:
            clear(id)
            for li in pics.children:
                liXmlObj = BeautifulSoup(str(li), "xml")
                if liXmlObj is not None:
                    if liXmlObj.li is not None:
                        liXml = liXmlObj.li
                        #大图
                        big_src = liXml.find('img').attrs['data-big']
                        print(big_src)
                        insert(id, big_src, i)
                        i = i + 1
            update(id, i)

    except AttributeError as e:
        print(e)
        return None
    return i


def insert(hid, src, num):
    cur.execute("insert into hotel_elong_pics(hotel_id, src, orders)\
                values(%s, %s, %s)",
                (hid, src, num))
    cur.connection.commit()


def clear(hid):
    cur.execute("delete from hotel_elong_pics where hotel_id = %s", hid)
    cur.connection.commit()


def update(hid, num):
    cur.execute("update hotel_elong \
                 set pics = %s\
                 where id = %s ",
                (num, hid))
    cur.connection.commit()

try:
    conn = pymysql.connect(host='localhost', user='root', passwd='rootroot', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE scrap")

    cur.execute("select id, city_pinyin from hotel_elong where pics = 0 order by create_time")
    i = 0
    # http://hotels.ctrip.com/hotel/427807.html
    for url in cur.fetchall():
        i = i+1
        if i % 20 == 0:
            print('%,休息一下', i)
            time.sleep(2)
        page = "http://hotel.elong.com/" + url[1] + "/" + str(url[0]) + "/"
        try:
            info = getPage(page, url[0])
            if info == None:
                print("get hotel detail error:%s", url[0])
                None
            else:
                print("-------------")

        except Exception as e:
            print(e)
            continue

except Exception as e:
        print(e)
        None
finally:
    cur.close()
    conn.close()
