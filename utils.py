# -*- coding: utf-8 -*-
import datetime
import functools
import json
import pprint
import random
import re
import time
import traceback

import requests
from prettytable import PrettyTable  # 命令行可视化表格
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm

"""
需要安装的模块 
pip install requests 
pip install tqdm
pip install prettytable
"""

# 禁止ssl证书验证警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 默认headers
default_headers = {
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,'
                  'likeGecko)Chrome/92.0.4515.131Safari/537.36',
    'sec-ch-ua': '"Chromium";v="92","NotA;Brand";v="99","GoogleChrome";v="92"',
    'sec-ch-ua-mobile': '?0'}


def tryError(fn):
    """
    装饰器 对被装饰的函数的运行try-catch
    :param fn: 被装饰的函数fn
    :return:
    """

    @functools.wraps(fn)  # 保持fn方法名字和文档不变
    def wrapper(*args, **kvargs):
        try:
            ret = fn(*args, **kvargs)
            return ret
        except Exception as e:
            # print("=========================")
            # msg = f'出错原因: {e.__doc__}  {e} \n函数名: {fn.__name__}\n函数说明: {fn.__doc__}'
            # print(msg)
            # print("=========================")
            # time.sleep(0.2)
            print(e)
            traceback.print_exc()

    return wrapper


def takeTime(fn):
    """
    装饰器 检测函数执行时间
    :param fn:
    :return:
    """

    @functools.wraps(fn)
    def wrapper(*args, **kvargs):  # *args, **kvargs 位置参数和关键字参数
        start = datetime.datetime.now()  # 函数运行开始时间
        ret = fn(*args, **kvargs)  # 函数运行
        end = datetime.datetime.now()  # 函数运行结束时间
        print(f'{fn.__name__} 耗费时间: {end - start} ')  # 打印执行时间
        return ret

    return wrapper


@tryError
def requireText(url: str, method: str, headers: dict = None, params: dict = None, data: dict = None) -> str:
    """
    获取返回的Text 仅在本模块内部使用
    :param url: url地址
    :param method: 请求方式
    :param headers: 请求头
    :param params: get字典参数
    :param data: post字典参数
    :return:
    """
    t_headers = headers if headers else default_headers  # 如果headers为None就使用默认的
    t_headers['Accept-Encoding'] = 'utf-8'  # 表明我只接受utf-8编码的Text文本
    with requests.session() as session:
        with session.request(method=method, url=url, headers=t_headers, verify=False, params=params, data=data) as resp:
            resp.encoding = resp.apparent_encoding  # 自动推断文本编码 不过由于我们之前在headers已经说明只接受utf-8了 所以有点多余
            return resp.text


def getText(url: str, headers: dict = None, params: dict = None, data: dict = None, showResult: bool = False) -> str:
    """
    以GET方式请求文本Text
    :param url:
    :param headers:
    :param params:
    :param data:
    :param showResult:  是否显示请求结果 默认不显示
    :return:
    """
    resultText = requireText(url=url, method='GET', headers=headers, params=params, data=data)
    if showResult:
        print(resultText)
    return resultText


def postText(url: str, headers: dict = None, params: dict = None, data: dict = None, showResult: bool = False) -> str:
    """
    以POST方式请求文本
    :param url:
    :param headers:
    :param params:
    :param data:
    :param showResult:  是否显示请求结果 默认不显示
    :return:
    """
    resultText = requireText(url=url, method='POST', headers=headers, params=params, data=data)
    if showResult:
        print(resultText)
    return resultText


def getJson(url: str, headers: dict = None, params: dict = None, data: dict = None, showResult: bool = False) -> dict:
    """
    GET方式请求Json文本,获取返回的Json对象
    间接调用getText 然后将返回的结果Json化
    :param url:
    :param headers:
    :param params:
    :param data:
    :param showResult:  是否显示请求结果 默认不显示
    :return:
    """
    jsonResult = json.loads(getText(url=url, headers=headers, params=params, data=data))
    if showResult:
        pprint.pprint(jsonResult)
    return jsonResult


def postJson(url: str, headers: dict = None, params: dict = None, data: dict = None, showResult: bool = False) -> dict:
    """
    POST,获取返回的Json对象
    间接调用getText 然后将返回的结果Json化
    :param url:
    :param headers:
    :param params:
    :param data:
    :param showResult:  是否显示请求结果 默认不显示
    :return:
    """
    jsonResult = json.loads(postText(url=url, headers=headers, params=params, data=data))
    if showResult:
        pprint.pprint(jsonResult)
    return jsonResult


@tryError
def getBytes(url: str, headers: dict = None) -> bytes:
    """
    从网络上面获取二进制字节流
    :param url:
    :param headers:
    :return:
    """
    t_headers = headers if headers else default_headers
    with requests.session() as session, session.get(url=url, headers=t_headers, stream=True, verify=False) as resp:
        return resp.content


def writeBytes(filePath: str, url: str, headers: dict = None) -> None:
    """
    从网络上面下载二进制文件到本地
    :param filePath:
    :param url:
    :param headers:
    :return:
    """
    with open(filePath, 'wb+') as wf:
        wf.write(getBytes(url=url, headers=headers))  # 简介调用getBin方法
    print(f'{filePath} down ok !')


def writeText(filePath: str, url: str, headers: dict = None, params: dict = None, data: dict = None,
              showResult: bool = False) -> None:
    """
    从网络上面下载文本文件到本地
    :param showResult: 是否显示返回结果
    :param data:
    :param params:
    :param filePath:
    :param url:
    :param headers:
    :return:
    """
    with open(filePath, 'w', encoding='utf-8') as wf:
        # 间接调用getText
        wf.write(getText(url=url, headers=headers, params=params, data=data, showResult=showResult))
    print(f'{filePath} down ok !')


def writeBytesBar(filePath: str, url: str, headers: dict = None) -> None:
    """
    从网络上面下载二进制文件到本地 使用tqdm库展示进度条
    :param filePath:
    :param url:
    :param headers:
    :return:
    """
    try:
        t_headers = headers if headers else default_headers
        with requests.session() as session, session.get(url=url, headers=t_headers, stream=True, verify=False) as resp:
            fileSize = int(resp.headers['content-Length'])
            with tqdm(initial=0, total=fileSize, unit_scale=True, unit='B') as pbar:
                with open(filePath, 'wb+') as wf:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            wf.write(chunk)
                            pbar.update(len(chunk))
                print(f'{filePath} down ok !')
    except Exception as e:
        print(e)
        traceback.print_exc()


@tryError
def getHeadersKV(pstr: str = '', pname: str = 'headers='):
    """
    从chrome直接复制的headers放在当前目录下的【getKV.txt】文件中
    运行一下就能直接得到字典类型的
    不用手动加引号了
    :param pstr:
    :param pname:
    :return:
    """
    filePath = 'getKV.txt'
    if pstr == '':
        with open(filePath, 'r', encoding='utf-8') as rf:
            string = rf.read()
    else:
        string = pstr
    s = string.replace(' ', '').splitlines()
    s = [item for item in s if item != '']  # 好像没有必要
    headers = {}
    for item in s:
        key = item.split(':')[0]
        value = item.replace(fr'{key}:', '').strip()
        headers[key] = value
    print(pname, end='')
    pprint.pprint(headers)


def removeBlank(pstr: str) -> str:
    """
    利用[正则表达式]移除字符串中的空白
    :param pstr:
    :return:
    """
    return re.sub(re.compile(r'\s+', re.S), '', pstr)


def getListByRe(restr: str, url: str, headers: dict = None, params: dict = None, data: dict = None,
                showResult: bool = False) -> list:
    """
    1.先进行网络请求
    2.利用正则表达式从返回的Text文本中提取出需要的东西
    3.找到所有符合条件的
    4.返回一个列表 列表中的元素是元组组 元素是每条获取的信息
    示例:
    getListByRe(restr=r'<script>(?P<getName>.*?)=(?P<getUrl>.*?)</script>', url='https://......')

    :param showResult:
    :param data:
    :param params:
    :param restr:
    :param url:
    :param headers:
    :return:
    """
    try:
        getHtml = getText(url=url, headers=headers, params=params, data=data)
        getHtml = removeBlank(getHtml)
        names = re.compile(r'P<(?P<getName>.*?)>', re.S).findall(restr)
        print(names)
        finditer = re.compile(restr, re.S).finditer(getHtml)
        tasks = []
        for item in finditer:
            task = []
            for name in names:
                task.append(item.group(name))
            tasks.append(tuple(task))
        if showResult:
            pprint.pprint(tasks)
        return tasks
    except Exception as e:
        print(e)
        traceback.print_exc()


def getSingleByRe(restr: str, url: str, headers: dict = None, params: dict = None, data: dict = None,
                  showResult: bool = False) -> tuple:
    """
    1.先进行网络请求
    2.利用正则表达式从返回的Text文本中提取出需要的东西
    3.找到第一个符合条件的
    4.返回一个元组
    示例:
    getListByRe(restr=r'<script>(?P<getName>.*?)=(?P<getUrl>.*?)</script>', url='https://......')
    :param showResult:
    :param data:
    :param params:
    :param restr:
    :param url:
    :param headers:
    :return:
    """
    try:
        getHtml = getText(url=url, headers=headers, params=params, data=data)
        getHtml = removeBlank(getHtml)
        names = re.compile(r'P<(?P<getName>.*?)>', re.S).findall(restr)
        search = re.compile(restr, re.S).search(getHtml)
        task = []
        for name in names:
            task.append(search.group(name))
        if showResult:
            pprint.pprint(tuple(task))
        return tuple(task)
    except Exception as e:
        print(e)
        traceback.print_exc()


def sleepShort(showSleepTime: bool = False):
    """
    在两次网络请求之间  随机短时间沉睡  防止服务器判断为爬虫
    :return:
    """
    ranTime = random.choice([0.4, 0.5, 0.6, 0.65, 0.55, 0.7])
    if showSleepTime:
        print(f"沉睡: {ranTime}s")
    time.sleep(ranTime)


def sleepLong(showSleepTime: bool = False):
    """
    在两次网络请求之间  随机长时间沉睡  防止服务器判断为爬虫
    :param showSleepTime:
    :return:
    """
    ranTime = random.choice([1.5, 2.0, 2.5, 3])
    if showSleepTime:
        print(f"沉睡: {ranTime}s")
    time.sleep(ranTime)


def sleepMedium(showSleepTime: bool = False):
    """
    在两次网络请求之间  随机中等时间沉睡  防止服务器判断为爬虫
    :param showSleepTime:
    :return:
    """
    ranTime = random.choice([1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6, 1.7, 1.8])
    if showSleepTime:
        print(f"沉睡: {ranTime}s")
    time.sleep(ranTime)


def printTable(rows: list, headers: list = None) -> None:
    """
    打印表格:
        import 本模块
        headers = ['Country', 'Capital', 'Population']
        rows = [["中文", "Beijing", 21893095], ["意大利是我去过的确定", "Moscow", 12195221], ["Germany", "Berlin", 3748148]]
        本模块.printTable(rows=rows, headers=headers)
    :param rows:
    :param headers:
    :return:
    """
    table = PrettyTable()
    if headers:
        if len(headers) != len(rows[0]):
            print("表格不对齐,行数或者列数不对劲")
            return
        table.field_names = headers
    else:
        h_size = len(rows[0])
        t_headers = []
        for index in range(1, h_size + 1):
            t_headers.append(f"第{index}列")
        table.field_names = t_headers
    for row in rows:
        table.add_row(row)
    print(table)


class BV_AV():
    """
    bilibili bv he av 转换
    """

    def __init__(self):
        self.table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        self.tr = {}
        for i in range(58):
            self.tr[self.table[i]] = i
        self.s = [11, 10, 3, 8, 4, 6]
        self.xor = 177451812
        self.add = 8728348608

    def dec(self, x):
        r = 0
        for i in range(6):
            r += self.tr[x[self.s[i]]] * 58 ** i
        return (r - self.add) ^ self.xor

    def enc(self, x):
        x = (x ^ self.xor) + self.add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[self.s[i]] = self.table[x // 58 ** i % 58]
        return ''.join(r)


def get_random_agent(index=None):
    agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36']
    if index:
        return agent_list[index]
    else:
        return random.choice(agent_list)


