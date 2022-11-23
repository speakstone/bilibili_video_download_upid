#!/usr/bin/env python
# encoding: utf-8
'''
@author: lee
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited. 
@contact: deamoncao100@gmail.com
@software: garner
@file: tools.py
@time: 2022/5/19 9:46
@desc:
'''
import requests, time, hashlib, urllib.request, re, json
from moviepy.editor import *
from utils import get_random_agent
import os, sys, threading
import ctypes
import platform
import zipfile, os
import math
import tarfile


class BV_AV():
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

    def enc(self,x):
        x = (x ^ self.xor) + self.add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[self.s[i]] = self.table[x // 58 ** i % 58]
        return ''.join(r)

# 访问API地址
def get_play_list(start_url, cid, quality):
    try:
        entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
        appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
        params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
        chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
        url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
        headers = {
            'Referer': start_url,  # 注意加上referer
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        html = requests.get(url_api, headers=headers).json()
        video_list = []
        for i in html['durl']:
            video_list.append(i['url'])
    except:
        return []
    return video_list


# 下载视频
'''
 urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''

class tools():
    def __init__(self):
        self.start_time = time.time()

    def Schedule_cmd(self, blocknum, blocksize, totalsize):
        speed = (blocknum * blocksize) / (time.time() - self.start_time)
        # speed_str = " Speed: %.2f" % speed
        speed_str = " Speed: %s" % self.format_size(speed)
        recv_size = blocknum * blocksize

        # 设置下载进度条
        f = sys.stdout
        pervent = recv_size / totalsize
        percent_str = "%.2f%%" % (pervent * 100)
        n = round(pervent * 50)
        s = ('#' * n).ljust(50, '-')
        f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
        f.flush()
        # time.sleep(0.1)
        f.write('\r')


    def Schedule(self,blocknum, blocksize, totalsize):
        speed = (blocknum * blocksize) / (time.time() - self.start_time)
        # speed_str = " Speed: %.2f" % speed
        speed_str = " Speed: %s" % self.format_size(speed)
        recv_size = blocknum * blocksize

        # 设置下载进度条
        f = sys.stdout
        pervent = recv_size / totalsize
        percent_str = "%.2f%%" % (pervent * 100)
        n = round(pervent * 50)
        s = ('#' * n).ljust(50, '-')
        print(percent_str.ljust(6, ' ') + '-' + speed_str)
        f.flush()
        time.sleep(2)


    def format_size(self,bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print("传入的字节格式不对")
            return "Error"
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%.3fG" % (G)
            else:
                return "%.3fM" % (M)
        else:
            return "%.3fK" % (kb)


    #  下载视频
    def down_video(self, video_list, title, start_url, page, save_path):
        num = 1
        print('[正在下载P{}段视频,请稍等...]:'.format(page) + title)
        currentVideoPath = os.path.join(save_path, title)  # 当前目录作为下载目录
        if not os.path.exists(currentVideoPath):
            os.makedirs(currentVideoPath)
        elif len(os.listdir(currentVideoPath)) > 0:
            print('文件{}已经存在，跳过此视频下载'.format(currentVideoPath))
            return
        for i in video_list:
            opener = urllib.request.build_opener()
            # 请求头
            opener.addheaders = [
                # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
                ('User-Agent', get_random_agent()),
                ('Accept', '*/*'),
                ('Accept-Language', 'en-US,en;q=0.5'),
                ('Accept-Encoding', 'gzip, deflate, br'),
                ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
                ('Referer', start_url),  # 注意修改referer,必须要加的!
                ('Origin', 'https://www.bilibili.com'),
                ('Connection', 'keep-alive'),
            ]
            urllib.request.install_opener(opener)
            # 创建文件夹存放下载的视频
            if not os.path.exists(currentVideoPath):
                os.makedirs(currentVideoPath)
            # 开始下载
            try:
                # if len(video_list) > 1:
                #     urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}-{}.flv'.format(title, num)),
                #                                reporthook=self.Schedule_cmd)  # 写成mp4也行  title + '-' + num + '.flv'
                # else:
                #     urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}.flv'.format(title)),
                #                                reporthook=self.Schedule_cmd)  # 写成mp4也行  title + '-' + num + '.flv'
                if len(video_list) > 1:
                    urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath,
                                                r'{}-{}.flv'.format(title, num))
                                               )  # 写成mp4也行  title + '-' + num + '.flv'
                else:
                    urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath,
                                                r'{}.flv'.format(title))
                                               )  # 写成mp4也行  title + '-' + num + '.flv'
                num += 1
            except:
                continue


    # 合并视频(20190802新版)
    def combine_video(self, title_list, video_path):
        # video_path = os.path.join(sys.path[0], 'bilibili_video')  # 下载目录
        for title in title_list:
            current_video_path = os.path.join(video_path ,title)
            if len(os.listdir(current_video_path)) >= 2:
                # 视频大于一段才要合并
                print('[下载完成,正在合并视频...]:' + title)
                # 定义一个数组
                L = []
                # 遍历所有文件
                for file in sorted(os.listdir(current_video_path), key=lambda x: int(x[x.rindex("-") + 1:x.rindex(".")])):
                    # 如果后缀名为 .mp4/.flv
                    if os.path.splitext(file)[1] == '.flv':
                        # 拼接成完整路径
                        filePath = os.path.join(current_video_path, file)
                        # 载入视频
                        video = VideoFileClip(filePath)
                        # 添加到数组
                        L.append(video)
                # 拼接视频
                final_clip = concatenate_videoclips(L)
                # 生成目标视频文件
                final_clip.to_videofile(os.path.join(current_video_path, r'{}.mp4'.format(title)), fps=24, remove_temp=False)
                print('[视频合并完成]' + title)
            else:
                # 视频只有一段则直接打印下载完成
                print('[视频合并完成]:' + title)


def get_free_space_mb(folder):
  """ Return folder/drive free space (in bytes)
  """
  if platform.system() == 'Windows':
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value/1024/1024/1024
  else:
    st = os.statvfs(folder)
    return st.f_bavail * st.f_frsize/1024/1024/1024





def tarDir(output_filename, source_dir):
    """
    一次性打包目录为tar.gz
    :param output_filename: 压缩文件名
    :param source_dir: 需要打包的目录
    :return: bool
    """
    try:
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

        return True
    except Exception as e:
        print(e)
        return False


def zip_file(source_file, outputfile_path=None, block_size=5000):
    """
    @para:source_file:源压缩文件夹的绝对路径
    @para:outputfile_path:压缩后的目录，
    @para:block_size:单位为Mbits,默认100Mbits
    @return:list，由压缩目录+f[i].zip组成的列表, i为分包数目
    """
    # 判断outputfile_path是否存在，不存在，则创建：
    if outputfile_path == None:
        outputfile_path = source_file + "_zip"
    if not os.path.exists(outputfile_path):
        os.mkdir(outputfile_path)
    size_Mbit=block_size*1024*1024
    file_size_temp=0
    count=1
    for dir_path, dir_name, file_names in os.walk(source_file):
        # 要是不replace，就从根目录开始复制
        file_path = dir_path.replace(source_file, "")
        # 实现当前文件夹以及包含的所有文件
        file_path = file_path and file_path + os.sep or ''
        for file_name in file_names:
            file_size_temp += os.path.getsize(os.path.join(dir_path, file_name))
    count_sum= math.ceil(file_size_temp /size_Mbit)
    print("大小为%sMbits, 分包数量为%s" % (file_size_temp /(1024*1024), count_sum))

    try:
        path_list=[]
        createVar = locals()
        for i in range(1,(count_sum+1)):
            zip= os.path.split(source_file)[-1] + "_" + str(i) +".zip"
            path_list.append(os.path.join(outputfile_path,zip))
            createVar['f'+ str(i)] = zipfile.ZipFile(os.path.join(outputfile_path,zip), 'w', zipfile.ZIP_DEFLATED)
        count=1
        file_size_temp=0
        for dir_path, dir_name, file_names in os.walk(source_file):
            # 要是不replace，就从根目录开始复制
            file_path = dir_path.replace(source_file, "")
            # 实现当前文件夹以及包含的所有文件
            file_path = file_path and file_path + os.sep or ''
            for file_name in file_names:
                file_size_temp += os.path.getsize(os.path.join(dir_path, file_name))
                if file_size_temp > size_Mbit:
                    count= count+1
                    file_size_temp=0
                createVar['f'+ str(count)].write(os.path.join(dir_path, file_name), file_path + file_name)
        for i in range(1,(count_sum+1)):
            createVar['f'+ str(i)].close()
        return path_list
    finally:
        for i in range(1,(count_sum+1)):
            createVar['f'+ str(i)].close()

# print(zip_file(r"/home/data/bili_results/13087547", block_size=2000))
# print(get_free_space_mb("/home/data"))