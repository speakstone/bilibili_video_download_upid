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
import tarfile
from utils import *
from tools import *

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


class bilidowload_upid():
    """
    根据up猪id进行批量下载
    """

    def __init__(self):
        self.save_path = "../bili_results/"  # 视频下载存放位置
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        self.user_agent_list = []
        self.tasks = []
        self.quality = 16  # 1080p:80;720p:64;480p:32;360p:16
        self.heards = {'accept': 'application/json, text/plain, */*',
                       'accept-encoding': 'utf-8',
                       'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,mn;q=0.6,en-GB;q=0.5',
                       'cookie': "buvid3=E9A5A7B5-1F50-7387-F96D-8A085D8CF50376403infoc; _uuid=BAF13D06-7569-9B79-DC06-F2752BD80B1077175infoc; video_page_version=v_old_home_19; blackside_state=1; rpdid=|(u~J~)lmYm)0J'uYJlRm~l)); CURRENT_QUALITY=64; buvid4=D5712071-7B09-103C-3DE5-79A72DEA104F39094-022012511-2JtCUEJkdYRDBDy5va0s2A%3D%3D; i-wanna-go-back=-1; nostalgia_conf=-1; CURRENT_BLACKGAP=0; fingerprint=4d5e0de30e1275a5a1bf5588a9d06511; buvid_fp_plain=undefined; buvid_fp=45947c7f9049298f39b5cc361fc13a41; DedeUserID=11815999; DedeUserID__ckMd5=93f6294bfbd19127; SESSDATA=ea35bc79%2C1667889525%2Cf85fc*51; bili_jct=f9333fc72a288411f61a83c1110d5011; b_ut=5; sid=hxfzosk8; bsource=search_google; LIVE_BUVID=AUTO5516528588951817; bp_video_offset_11815999=661460616157855900; innersign=1; CURRENT_FNVAL=4048; b_lsid=E1DE6F3E_180D64C5B3A; b_timer=%7B%22ffp%22%3A%7B%22333.788.fp.risk_E9A5A7B5%22%3A%22180D64B23F9%22%2C%22333.1007.fp.risk_E9A5A7B5%22%3A%22180D639D520%22%2C%22333.976.fp.risk_E9A5A7B5%22%3A%22180D6109AE9%22%2C%22333.337.fp.risk_E9A5A7B5%22%3A%22180D61C1F3A%22%2C%22333.999.fp.risk_E9A5A7B5%22%3A%22180D66160A3%22%2C%22888.2421.fp.risk_E9A5A7B5%22%3A%22180D639C228%22%2C%22777.5.0.0.fp.risk_E9A5A7B5%22%3A%22180D63A26A9%22%7D%7D; PVID=4",
                       'dnt': '1',
                       'origin': 'https://space.bilibili.com',
                       'referer': 'https://space.bilibili.com/1583156357/video',
                       'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                       'sec-ch-ua-mobile': '?0',
                       'sec-ch-ua-platform': "Windows",
                       'sec-fetch-dest': 'empty',
                       'sec-fetch-mode': 'cors',
                       'sec-fetch-site': 'same-site',
                       'user-agent': ""}


        self.params = {'mid': "",
                       'pn': 1,
                       'ps': 30,
                       'index': 1,
                       'jsonp': 'jsonp'}

        self.url = 'https://api.bilibili.com/x/space/arc/search'

        self.bilitools = tools()

    def getUpAllBvide(self):
        """
        根据us id获取到当前页的所有video id
        :param usid:
        :return:
        """
        getJson_ = getJson(url=self.url, headers=self.heards, params=self.params)
        if str(getJson_['code']) == "0":
            self.tasks = getJson_['data']['list']['vlist']
            self.params['pn'] += 1
        if len(self.tasks) < self.params['ps']:
            return False
        return True

    def download_cid(self, cid_list):
        start_time = time.time()
        # 创建线程池
        title_list = []
        for item in cid_list:
            cid = str(item['cid'])
            title = item['part']
            title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
            # print('[下载视频的cid]:' + cid)
            # print('[下载视频的标题]:' + title)
            title_list.append(title)
            page = str(item['page'])
            start_url = self.start_url + "/?p=" + page
            video_list = get_play_list(start_url, cid, self.quality)
            start_time = time.time()
            save_dir = os.path.join(self.save_path, self.params['mid'])
            if not os.path.isdir(save_dir):
                os.mkdir(save_dir)
            self.bilitools.down_video(video_list, title, start_url, page, save_dir)
        #     # 定义线程
        #     th = threading.Thread(target=self.bilitools.down_video, args=(video_list, title, start_url, page, self.save_path))
        #     # 将线程加入线程池
        #     threadpool.append(th)
        #
        # # 开始线程
        # for th in threadpool:
        #     th.start()
        # # 等待所有线程运行完毕
        # for th in threadpool:
        #     th.join()
        end_time = time.time()  # 结束时间
        print('下载总耗时%.2f秒,约%.2f分钟' % (end_time - start_time, int(end_time - start_time) / 60))

    def download_usid(self, usid):
        """
        下载主函数
        :param usid:
        :return:
        """
        self.heards['user-agent'] = get_random_agent()
        self.params['mid'] = usid
        while True:
            last_page = self.getUpAllBvide()
            vids = [[i["aid"], i["bvid"]] for i in self.tasks]
            for index, vid in enumerate(vids):
                self.bilitools = tools()
                avid = vid[0]
                self.start_url = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(avid)
                html = requests.get(self.start_url, headers={'User-Agent':  get_random_agent()}).json()
                data = html['data']['pages']
                self.download_cid(data)
                time.sleep(random.random() + 2)
                # print(data)
            if not last_page:
                tarDir(os.path.join(self.save_path, str(usid)) + '.tar.gz', self.save_path)
                break


if __name__ == "__main__":
    main = bilidowload_upid()
    usid_list = []
    if len(usid_list) == 0:
        usid = input('请输入您要下载的B站up猪的id:')
        main.download_usid(str(usid))
    else:
        for usid in usid_list:
            main.download_usid(str(usid))
