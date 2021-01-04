# -*- coding: utf-8 -*-
# @ProjectName: PycharmProjects
# @File: BVNum.py
# @Author: Lyn
# @Date: 2020/11/17 10:16
# @IDE: PyCharm
# @Version: 1.0
# @Function:
import json
import re
import time

import requests
from bs4 import BeautifulSoup


class bVNum:
    _urlPage = "https://kanbilibili.com/weekly?page="
    _url = "https://kanbilibili.com/json/weekly/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 Safari/537.36'}
    bvIdList = []
    dateList = []
    commentList = []

    def __init__(self):
        self.bvIdList = []
        self.dateList = []
        self.commentList = []

    def readPage(self, num):
        urlPage = self._urlPage + str(num)
        response = requests.get(urlPage, headers=self.headers).content.decode()
        html = BeautifulSoup(response, "html.parser")
        dateTag = html.select('img[class="pic"]')
        patternDate = re.compile('alt="(.*?)"')
        _dateList = patternDate.findall(str(dateTag))
        for _date in _dateList:
            _date = _date.replace("年", "").replace("月", "").replace("日", "")
            self.dateList.append(_date)

    # https://kanbilibili.com/json/weekly/20200726/1_play_0.json
    # https://kanbilibili.com/api/weekly/20200726?offset=30&tid=1
    def readBvNum(self, _date, num):
        time.sleep(5)
        url = self._url + str(_date) + "/" + str(num) + "_play_0.json"
        response = requests.get(url, headers=self.headers)
        text = response.text
        jsonList = json.loads(text)
        for i in range(30):
            jsonText = jsonList[i]
            bvId = jsonText['aid']
            self.bvIdList.append(bvId)
            comment = jsonText['reviewTotal']
            self.commentList.append(comment)
        url2 = "https://kanbilibili.com/api/weekly/" + str(_date) + "?offset=30&tid=" + str(num)
        response2 = requests.get(url2, headers=self.headers, )
        text2 = response2.text
        if text2[0] == "{":
            jsonList2 = json.loads(text2)
            dataList = jsonList2['data']
            for i in range(70):
                self.bvIdList.append(dataList[i]['aid'])
                self.commentList.append(dataList[i]['reviewTotal'])

# if __name__ == '__main__':
#     bvNum = bVNum()
#     # 参数是页数
#     bvNum.readPage(1)
#     dateList = bvNum.dateList
#     for date in dateList:
#         # 参数    分区
#         # 1      动画
#         # 3      音乐
#         # 4      游戏
#         # 5      娱乐
#         # 36     科技
#         # 119    鬼畜
#         # 129    舞蹈
#         # 155    时尚
#         # 160    生活
#         bvNum.readBvNum(date, 1)
