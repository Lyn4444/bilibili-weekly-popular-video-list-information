# -*- coding: utf-8 -*-
# @ProjectName: PycharmProjects
# @File: Bilibili.py
# @Author: Lyn
# @Date: 2020/11/9 17:41
# @IDE: PyCharm
# @Version: 1.0
# @Function:
import time

import openpyxl
import requests
from bs4 import BeautifulSoup
import re
import xlrd
from xlutils.copy import copy
import os

from BVNum import bVNum


class Crawler:
    bvIdList = []
    url = "https://www.bilibili.com/video/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 Safari/537.36'}
    xlsxDate = ""

    def __init__(self, xlsxDate):
        self.bvIdList = []
        self.xlsxDate = xlsxDate

    def connection(self, BVNumber, comment):
        self.url += BVNumber
        response = requests.get(self.url, headers=self.headers).content.decode()
        html = BeautifulSoup(response, "html.parser")
        upName = html.select('a[report-id="name"]')
        patternUid = re.compile('href="//space.bilibili.com/(.*?)"')
        uid = patternUid.findall(str(upName))
        if uid.__len__() > 0:
            uid = uid[0]
        else:
            uid = "联合创作"
        if upName.__len__() > 0:
            upName = upName[0].get_text()
        else:
            upName = "联合创作"
        data = str(html.select('div[class="video-data"]'))
        patternDate = re.compile('<span>(.*?)</span>')
        patternCommon = re.compile('title="(.*?)"')
        date = patternDate.findall(data)
        if date.__len__() > 0:
            date = date[0]
        else:
            date = "不存在"
        view = patternCommon.findall(str(html.select('span[class="view"]')))
        if view.__len__() > 0:
            view = view[0]
        else:
            view = "不存在"
        dm = patternCommon.findall(str(html.select('span[class="dm"]')))
        if dm.__len__() > 0:
            dm = dm[0]
        else:
            dm = "不存在"
        title = None
        _title = html.select('span[class="tit"]')
        if _title.__len__() > 0:
            title = _title[0].get_text().replace("\n", "").strip()
        _title = html.select('span[class="tit tr-fix"]')
        if _title.__len__() > 0:
            title = _title[0].get_text().replace("\n", "").strip()
        brief = html.select('div[class="info open"]')
        if brief.__len__() > 0:
            brief = brief[0].get_text().replace("\n", "").strip()
        else:
            brief = "需要人为输入"
        tagRemarkable = ""
        tagRemarkableTemp = html.select('span[class="channel-name"]')
        for i in tagRemarkableTemp:
            tagRemarkable = tagRemarkable + i.get_text() + " "
        tagLink = ""
        tagLinkTemp = html.select('a[class="tag-link"]')
        for i in tagLinkTemp:
            temp = i.get_text().replace("\n", "").strip()
            tagLink = tagLink + temp + " "
        like = "不存在"
        _like = html.select('span[class="like"]')
        if _like.__len__() > 0:
            _like = _like[0]
            _like = str(_like)
            _like = _like.replace("\n", "").replace("\t", "")
            patternLike = re.compile(r'</i>(.*?)</span>')
            _like = patternLike.findall(_like)
            like = _like[0].strip()
        coin = "不存在"
        _coin = html.select('span[class="coin"]')
        if _coin.__len__() > 0:
            _coin = _coin[0]
            _coin = str(_coin)
            _coin = _coin.replace("\n", "").replace("\t", "")
            patternCoin = re.compile(r'</i>(.*?)</span>')
            _coin = patternCoin.findall(_coin)
            coin = _coin[0].strip()
        collect = "不存在"
        _collect = html.select('span[class="collect"]')
        if _collect.__len__() > 0:
            _collect = _collect[0]
            _collect = str(_collect)
            _collect = _collect.replace("\n", "").replace("\t", "")
            patternCollect = re.compile(r'</i>(.*?)</span>')
            _collect = patternCollect.findall(_collect)
            collect = _collect[0].strip()
        _share = html.select('span[class="share"]')
        _share = str(_share)
        _share = _share.replace("\n", "").replace("\t", "")
        patternShare = re.compile(r'</i>(.*?)</span>')
        _share = patternShare.findall(_share)
        share = "不存在"
        if _share.__len__() > 0:
            _share = _share[0].replace("<!-- -->", "")
            share = _share.strip()
        dataList = [BVNumber, uid, upName, date, view, dm,
                    title, brief, tagRemarkable, tagLink, like, coin, collect, share, comment]
        xlsxName = "bilibili" + self.xlsxDate + ".xls"
        if os.path.exists(xlsxName):
            workbook = xlrd.open_workbook(xlsxName)
            sheetName = workbook.sheet_names()
            worksheet = workbook.sheet_by_name(sheetName[0])  # 获取工作薄中的第一个sheet
            rows_exists = worksheet.nrows  # 获取已经存在的数据行数
            new_workbook = copy(workbook)
            new_worksheet = new_workbook.get_sheet(0)
            for i in range(len(dataList)):
                new_worksheet.write(rows_exists, i, dataList[i])
            new_workbook.save(xlsxName)
        else:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            dataTitle = ['BV', 'uid', 'upName', 'date', 'view', 'danmu', 'title', 'brief', 'tagRemarkable', 'tagLink', 'like', 'coin', 'collect', 'share', 'comment']
            for i in range(0, len(dataTitle)):
                sheet.cell(1, i + 1, dataTitle[i])
            workbook.save(xlsxName)
            workbook = xlrd.open_workbook(xlsxName)
            sheetName = workbook.sheet_names()
            worksheet = workbook.sheet_by_name(sheetName[0])  # 获取工作薄中的第一个sheet
            rows_exists = worksheet.nrows  # 获取已经存在的数据行数
            new_workbook = copy(workbook)
            new_worksheet = new_workbook.get_sheet(0)
            for i in range(len(dataList)):
                new_worksheet.write(rows_exists, i, dataList[i])
            new_workbook.save(xlsxName)


if __name__ == '__main__':
    # BvList = bVNum()
    # BvList.readPage(1)
    # dateList = BvList.dateList
    # BvList.readPage(2)
    # dateList += BvList.dateList
    dateList = ['20191229', '20191222', '20191215', '20191208', '20191124', '20191117', '20191110', '20191103', '20191027', '20191013', '20190825', '20190811', '20190728', '20190623', '20190616', '20190526', '20190519', '20190210', '20190203', '20190127', '20200726', '20200621', '20200614', '20200517', '20200510', '20200503', '20200419', '20200412', '20200126', '20200105', '20191229', '20191222', '20191215', '20191208', '20191124', '20191117', '20191110', '20191103', '20191027', '20191013', '20190825', '20190811', '20190728', '20190623', '20190616', '20190526', '20190519', '20190210', '20190203', '20190127']
    print(dateList)
    print(dateList.__len__())
    for date in dateList:
        print(date)
        print("_____________")
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
        getBVNum = bVNum()
        getBVNum.readBvNum(date, 4)
        for i in range(getBVNum.bvIdList.__len__()):
            bvId = getBVNum.bvIdList[i]
            print(bvId)
            comment = getBVNum.commentList[i]
            crawler = Crawler(date)
            bvId = "av" + str(bvId)
            crawler.connection(bvId, comment)
            time.sleep(2)
