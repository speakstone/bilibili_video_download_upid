#!/usr/bin/env python
# encoding: utf-8
'''
@author: lee
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: main.py
@time: 2022/5/19 9:48
@desc:
'''

import urllib.request
from urllib import parse
import re
import json
from bs4 import BeautifulSoup

class up_id_get():
    """
    根据up猪id进行批量下载
    """
    def __init__(self, id):
        self.id = id.replace("x", "X").strip()
        self.url = 'http://120.48.51.8:11000/center/add?name={}'.format(self.id)

    def get_new_id(self):
        url_a = urllib.request.urlopen(self.url)  # 打开网址
        html = url_a.read().decode('utf-8')  # 读取源代码并转为unicode
        new_id = html.split("<span>最新分配: </span>")[1].split("</a></li>")[0]
        if self.id == new_id.split(",")[-2].strip() and new_id.split(",")[-1].strip() != 'done':
            return new_id.split(",")[1].strip()
        return False

    def up_id_statu(self, upid):
        self.done_url = 'http://120.48.51.8:11000/center/done?name={}'.format(upid)
        urllib.request.urlopen(self.done_url)  # 打开网址


def get_up_with_keyword(keyword):
    """
    根据up猪id进行批量下载
    """
    # "https://search.bilibili.com/all?keyword=%E5%B0%8F%E7%B1%B3%E5%8F%91%E5%B8%83%E4%BC%9A&from_source=webtop_search&spm_id_from=333.1007"
    upid_name = dict()
    keyword = parse.quote(keyword, encoding='utf-8')
    url = 'https://search.bilibili.com/all?keyword={}&from_source=webtop_search&spm_id_from=333.1007'.format(keyword)
    url_a = urllib.request.urlopen(url)  # 打开网址
    html = url_a.read().decode('utf-8')  # 读取源代码并转为unicode
    "bili-video-card__info--owner"
    # re.findall(r'<title>(.*?)</title>', html)
    soup = BeautifulSoup(html) # BeautifulSoup类
    soup_f = soup.find_all(class_="so-icon", title="up主") # 获取up主类
    for soup_i in soup_f:
        upid = re.search(r'com/(.*?)\?from=', soup_i.find("a").attrs['href'], re.M|re.I)[1]
        upname = soup_i.find("a").string
        upid_name[upid] = upname
    return upid_name



if __name__ == "__main__":
    # a = up_id_get("X6024")
    # new_id = a.get_new_id()
    # print(new_id)
    # a.up_id_statu(new_id.split(",")[1].strip())
    upid_name = get_up_with_keyword("发布会")


