# -*- coding = utf-8 -*-
# @TIME :2022/4/19 21:40
# @Author :CrescentLove
# @Software :PyCharm

# -*- coding = utf-8 -*-
# @TIME :2022/4/16 13:29
# @Author :CrescentLove
# @Software :PyCharm
import datetime
import json
import random
import string
import threading
from time import sleep
from requests_toolbelt import MultipartEncoder

import requests
from winsound import Beep
# hairCookie = 'agreeChecked=true; JSESSIONID=E2FEE84FB04D54A78EC69924ECCEEC5A; _ga=GA1.3.358036560.1616338531; UM_distinctid=17ce3baaa74600-02908cdd167d45-561a135a-fa000-17ce3baaa75662; dailyreport.sjtu=ffffffff097e1f5545525d5f4f58455e445a4a4229a0'
hairCookie = 'agreeChecked=true; JSESSIONID=A3946EEFE698D0542FCF1667E0F633C4; _ga=GA1.3.358036560.1616338531; UM_distinctid=17ce3baaa74600-02908cdd167d45-561a135a-fa000-17ce3baaa75662; _gid=GA1.3.1460440879.1650205309; dailyreport.sjtu=ffffffff097e1f5045525d5f4f58455e445a4a4229a0'
superCookie = 'agreeChecked=true; JSESSIONID=96A658AF7277FEDAE09917FDF9A71412; _ga=GA1.3.358036560.1616338531; UM_distinctid=17ce3baaa74600-02908cdd167d45-561a135a-fa000-17ce3baaa75662; dailyreport.sjtu=ffffffff097e1f5545525d5f4f58455e445a4a4229a0'

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
spicyHeader = {
    'cookie': superCookie,
    'user-agent' : userAgent
}
# confirmHeader = {
#             'User-Agent': userAgent,
#             'Cookie': hairCookie,
#             'Referer': 'https://dailyreport.sjtu.edu.cn/haircut/',
#             'Accept': 'application/json, text/plain, */*',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#             'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryCN7RyiGkXHpkehUY'}
# confirmUrl = 'https://dailyreport.sjtu.edu.cn/haircut/frontend/bus/appointment/save'
confirmUrlS = 'https://dailyreport.sjtu.edu.cn/market/frontend/market/appointment/save'

lineType = ['TWO', 'THIRD', 'FOURTH']
month = 4
day = 17
listUrl = 'https://dailyreport.sjtu.edu.cn/haircut/frontend/bus/schedule/list?'
listParam = {
    'lineType': lineType[1],
    'date': f'2022-{month}-{day}'
}

def getList(param):
    """

    :param param:
    :return:
    """

    while (1):
        timeNow = datetime.datetime.now().strftime('%H%M%S')
        # print('正在抢')
        if timeNow != '203000' and timeNow != '202999' and timeNow != '203001':
        # if 0:
            continue
        else:

            res = requests.get(url=f'https://dailyreport.sjtu.edu.cn/market/frontend/market/schedule/list?{param}', headers=spicyHeader)
            if res.status_code == 200:
                print('get')
                hairResp = res.json()['entities']
                for i in hairResp:
                    if i['leftSeat'] != 0:
                        hairId = i['id']
                        getOne(hairId)
                        sleep(0.2)
            else:
                print('getERROR',res.status_code, res.text)
        if timeNow == '203005' or timeNow == '203006' :
            break

def getList2(param):
    while (1):
        res = requests.get(url=f'https://dailyreport.sjtu.edu.cn/market/frontend/market/schedule/list?{param}', headers=spicyHeader)
        if res.status_code == 200:
            hairResp = res.json()['entities']
            print('正在抢')
            for i in hairResp:
                if i['leftSeat'] != 0:
                    hairId = i['id']
                    getOne(hairId)
        else:
            print('list',res.status_code,'\n',res.text)
        sleep(8)

def getOne(id,):
    fields = {'busScheduleId': id}
    boundary = '----WebKitFormBoundary' \
               + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {
        "Host": "dailyreport.sjtu.edu.cn",
        "Connection": "keep-alive",
        "Content-Type": m.content_type,
        'User-Agent': userAgent,
        'Cookie': superCookie,
        'Referer': 'https://dailyreport.sjtu.edu.cn/market/?locale=zh',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    # dataJson = json.dumps({'busScheduleId':id})
    res = requests.post(confirmUrlS,headers=headers,data=m)
    print('post', res.text, res.status_code)
    if (res.status_code == 200):
        resId = res.json()['entities'][0]
        print(resId)
    Beep(1000, 1000)

if __name__ == '__main__':
    alth = []
    sp = []

    for i in range(18):
        sp.append(f'lineType=TWO&date=2022-04-{i}')
        sp.append(f'lineType=THIRD&date=2022-04-{i}')
        sp.append(f'lineType=FOURTH&date=2022-04-{i}')

    # for i in range(len(sp)):
    #     alth.append(threading.Thread(target=getList2, args=(sp[i],)))
    #
    # for th in alth:
    #     th.start()
    #
    # for th in alth:
    #     th.join()

    getList2('lineType=DQJYCS&date=2022-04-22')
