# -*- coding:utf-8 -*-
__author__ = 'Shaun'
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pymysql
import time


class Info:
    def __init__(self):
        self.name = ''      # 名称
        self.title = ''     # 标题
        self.phone = ''     # 电话
        self.city = ''      # 城市
        self.district = ''  # 地区
        self.address = ''   # 地址
        self.star = ''      # 星级
        self.description = '' # 描述


def getPage(url):
    info = Info()
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")

        # 获取酒店标题
        title = bsObj.head.title.string
        print(title.strip())
        info.title = title.strip()

        # 获取酒店名称
        name = bsObj.find(id="lastbread")
        print(name.text.strip())
        info.name = name.text.strip()

        # 获取酒店描述
        description = bsObj.find("meta", {"name": "description"}).attrs["content"]
        print(description)
        info.description = description.strip()

        # 获取酒店星级
        star_raw = bsObj.find("b", {"class": "icon_stars"})
        if star_raw is not None:
            star = star_raw.attrs["title"]
            print(star)
            info.star = star

        # 获取酒店地址
        # address = bsObj.find("span", {"class": "mr5 left"}).text
        # print(address.strip())
        # info.address = address.strip()
        address = title[title.index('地址:')+3: title.index(' – 艺龙旅行网')]
        if address is None:
            address = bsObj.find("span", {"class": "mr5 left"}).text
        print(address.strip())
        info.address = address.strip()

        # 获取酒店电话
        phone = bsObj.find("i", {"class": "icon_view_s1"}).parent.parent.dd.text
        print(phone.replace("艺龙电话预订：4009-333-333","").strip())
        info.phone = phone.replace("艺龙电话预订：4009-333-333","").strip()

        # 获取酒店图片


    except AttributeError as e:
        print(e)
        return None
    return info


def update(hid, star, name, title, phone, description, address):
    cur.execute("update hotel_elong \
                 set star = %s ,name = %s ,title = %s ,phone = %s, description = %s, address=%s\
                 where id = %s ",
                (star, name, title, phone, description, address, hid))
    cur.connection.commit()

try:
    conn = pymysql.connect(host='localhost', user='root', passwd='rootroot', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE scrap")

    cur.execute("select id, city_pinyin from hotel_elong where name is null order by create_time")
    i = 0
    # http://hotels.ctrip.com/hotel/427807.html
    for url in cur.fetchall():
        i = i+1
        if i % 20 == 0:
            print('%,休息一下', i)
            time.sleep(2)
        page = "http://hotel.elong.com/" + url[1] + "/" + str(url[0]) + "/"
        try:
            info = getPage(page)
            if info == None:
                print("get hotel detail error:%s", url[0])
                None
            else:
                print("-------------")
                update(url[0], info.star, info.name, info.title, info.phone, info.description, info.address)

        except Exception as e:
            print(e)
            continue

except Exception as e:
        print(e)
        None
finally:
    cur.close()
    conn.close()
