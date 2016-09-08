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
#北京
cityName = '北京'
cityId = "0101"
cityPinYin = 'beijing'
cnt = 400

#杭州
# cityName = '杭州'
# cityId = "1201"
# cityPinYin = 'hangzhou'
# cnt = 200

#上海
# cityName = '上海'
# cityId = "0201"
# cityPinYin = 'shanghai'
# cnt = 320

#南京
# cityName = '南京'
# cityId = "1101"
# cityPinYin = 'nanjing'
# cnt = 200

headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':'1654',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'newjava2=dbbd747eaa27e55bb966708aaadf0d77; CookieGuid=5060cb54-61af-44d6-b5ce-f0c2d5c06903; SessionGuid=f9ff9816-2b46-402a-ab3b-15035b0f5be2; Esid=293d628c-4144-4feb-a26e-dba4ff5c3dd7; SHBrowseHotel=cn=40101032%2C%2C%2C%2C%2C%2C%3B; TLTSID=DBE967E5408F81E8A6F675ABA36F7C45; TLTHID=AB96D27141CDB5CB663D55A0FB385BC4; CitySearchHistory=0101%23%E5%8C%97%E4%BA%AC%23beijing%230%7C0; JSESSIONID=9EC5BF4446A423A89E3EBF21C06D75FB; _pk_ref.2624.9f06=%5B%22%22%2C%22%22%2C1471135583%2C%22http%3A%2F%2Fwww.elong.com%2F%22%5D; ShHotel=CityID=0101&CityNameCN=%E5%8C%97%E4%BA%AC%E5%B8%82&CityName=%E5%8C%97%E4%BA%AC%E5%B8%82&OutDate=2016-08-19&CityNameEN=Beijing&InDate=2016-08-18; s_cc=true; s_visit=1; s_sq=%5B%5BB%5D%5D; _pk_id.2624.9f06=b17d9a530ebfc89a.1471133228.2.1471135589.1471135583.; _pk_ses.2624.9f06=*; com.eLong.CommonService.OrderFromCookieInfo=Status=1&Orderfromtype=1&Isusefparam=0&Pkid=50&Parentid=50000&Coefficient=0.0&Makecomefrom=0&Cookiesdays=0&Savecookies=0&Priority=8000',
    'Host':'hotel.elong.com',
    'Origin':'http://hotel.elong.com',
    'Referer':'http://hotel.elong.com/search/list_cn_0101.html?aioIndex=-1&aioVal=',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}

# url = "http://hotel.elong.com/ajax/list/getmergedata"
url = "http://hotel.elong.com/ajax/list/asyncsearch"

conn = pymysql.connect(host='localhost', user='root', passwd='rootroot', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scrap")

for i in range(1,cnt):
    params = {
        'listRequest.areaID':'',
        'listRequest.bookingChannel':'1',
        'listRequest.cardNo':'192928',
        'listRequest.checkInDate':'2016-08-24 00:00:00',
        'listRequest.checkOutDate':'2016-08-25 00:00:00',
        'listRequest.cityID':cityId,
        'listRequest.cityName':cityName,
        'listRequest.customLevel':'11',
        'listRequest.distance':'20',
        'listRequest.endLat':'0',
        'listRequest.endLng':'0',
        'listRequest.facilityIds':'',
        'listRequest.highPrice':'0',
        'listRequest.hotelBrandIDs':'',
        'listRequest.isAdvanceSave':False,
        'listRequest.isAfterCouponPrice':True,
        'listRequest.isCoupon':False,
        'listRequest.isDebug':False,
        'listRequest.isLimitTime':False,
        'listRequest.isLogin':False,
        'listRequest.isMapSearch':False,
        'listRequest.isMobileOnly':True,
        'listRequest.isNeed5Discount':True,
        'listRequest.isNeedNotContractedHotel':False,
        'listRequest.isNeedSimilarPrice':False,
        'listRequest.isPrepay':False,
        'listRequest.isReturnNoRoomHotel':True,
        'listRequest.isStaySave':False,
        'listRequest.isTrace':False,
        'listRequest.isUnionSite':False,
        'listRequest.keywords':'',
        'listRequest.keywordsType':'0',
        'listRequest.language':'cn',
        'listRequest.lowPrice':'0',
        'listRequest.orderFromID':'50',
        'listRequest.pageIndex':i,
        'listRequest.pageSize':'20',
        'listRequest.personOfRoom':'0',
        'listRequest.poiId':'0',
        'listRequest.promotionChannelCode':'0000',
        'listRequest.proxyID':'ZD',
        'listRequest.rankType':'0',
        'listRequest.sellChannel':'1',
        'listRequest.sortDirection':'1',
        'listRequest.sortMethod':'1',
        'listRequest.starLevels':'',
        'listRequest.startLat':'0',
        'listRequest.startLng':'0',
        'listRequest.taRecommend':False,
        'listRequest.themeIds':'',
        # 'listRequest.hotelIDs':''
    }

    if i % 20 == 0:
        print('%,休息一下', i)
        time.sleep(1)
    try:
        r = requests.request('post', url=url, data=params, headers=headers)
        m = json.loads(r.text, encoding='utf-8')
        page_ret = json.dumps(m, ensure_ascii=False)
        doc = json.loads(page_ret, encoding='utf-8')
        hotel_strs = doc.get("value").get("hotelIds")
        hotel_list = hotel_strs.split(',')
        for hotel in hotel_list:
            print(hotel)
            try:
                cur.execute("insert into hotel_elong(id, city, city_pinyin, create_time)\
                        values(%s, %s, %s, now())",
                            (hotel, cityName, cityPinYin))
                cur.connection.commit()
            except Exception as e:
                print(e)
                continue
    except Exception as e:
            print('第', i, '页出现异常', e)
            continue
