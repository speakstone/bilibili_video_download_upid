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
import re


class up_id_get():
    """
    根据up猪id进行批量下载
    """
    def __init__(self, id):
        self.id = id.replace("x", "X").strip()
        self.url = 'http://10.1.203.191:11000/center/add?name={}'.format(self.id)

    def get_new_id(self):
        url_a = urllib.request.urlopen(self.url)  # 打开网址
        html = url_a.read().decode('utf-8')  # 读取源代码并转为unicode
        new_id = html.split("<span>最新分配: </span>")[1].split("</a></li>")[0]
        if self.id == new_id.split(",")[-2].strip() and new_id.split(",")[-1].strip() != 'done':
            return new_id.split(",")[1].strip()
        return False

    def up_id_statu(self, upid):
        self.done_url = 'http://10.1.203.191:11000/center/done?name={}'.format(upid)
        urllib.request.urlopen(self.done_url)  # 打开网址


if __name__ == "__main__":
    a = up_id_get("X6024")
    new_id = a.get_new_id()
    print(new_id)
    a.up_id_statu(new_id.split(",")[1].strip())


