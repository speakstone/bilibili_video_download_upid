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

    def __init__(self,save_path = "bili_results/", quality = 32):
        self.save_path = save_path  # 视频下载存放位置
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        self.tasks = []
        self.quality = quality  # 1080p:80;720p:64;480p:32;360p:16
        self.heards = {'accept': 'application/json, text/plain, */*',
                       'accept-encoding': 'utf-8',
                       'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,mn;q=0.6,en-GB;q=0.5',
                       'cookie': "buvid3=49BD1FE1-34D4-431D-99EB-D8DB9A29189D18551infoc; rpdid=|(umY))kRl~Y0J'uYJuYkYYRu; fingerprint3=94ccb0cdc423808508fe2f0db8ecf24c; fingerprint_s=71170c3052b75dda080fdd64dc92cbd6; i-wanna-go-back=-1; buvid4=C655A1DA-2AB1-693E-4EA1-2F6FED7F0F1A68995-022040121-Oji4gbak2AAKKjApcPakVA%3D%3D; nostalgia_conf=-1; CURRENT_BLACKGAP=0; _uuid=B10EB610B9-10CF3-CE16-577B-10CC107CEEC9DC95698infoc; LIVE_BUVID=AUTO8616501631623626; fingerprint=63a60485f955c87dae45ba270fbfbe1e; buvid_fp_plain=undefined; DedeUserID=11815999; DedeUserID__ckMd5=93f6294bfbd19127; SESSDATA=07c7ede8%2C1667813168%2C43c30*51; bili_jct=91397e35dce099400f14f1a8a7613cdf; buvid_fp=63a60485f955c87dae45ba270fbfbe1e; b_ut=5; b_lsid=FC916FEE_181058C0720; sid=5asvug23; innersign=1; blackside_state=0; bsource=search_google; PVID=2; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_49BD1FE1%22%3A%22181058C0E84%22%2C%22333.788.fp.risk_49BD1FE1%22%3A%22181058C3885%22%2C%22333.999.fp.risk_49BD1FE1%22%3A%22181058C5CBA%22%2C%22777.5.0.0.fp.risk_49BD1FE1%22%3A%22181058C60E0%22%2C%22888.2421.fp.risk_49BD1FE1%22%3A%2218105930870%22%2C%22333.976.fp.risk_49BD1FE1%22%3A%2218105935D9A%22%2C%22333.337.fp.risk_49BD1FE1%22%3A%22181059CF1AD%22%7D%7D; CURRENT_FNVAL=4048; CURRENT_QUALITY=80",
                        'dnt': '1',
                       'origin': 'https://space.bilibili.com',
                       'referer': '',
                       'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
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
                       'order': 'pubdate',
                       'tid': 0,
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
            title_list.append(title)
            page = str(item['page'])
            start_url = self.start_url + "/?p=" + page
            video_list = get_play_list(start_url, cid, self.quality)
            start_time = time.time()
            save_dir = os.path.join(self.save_path, self.params['mid'])
            if not os.path.isdir(save_dir):
                os.mkdir(save_dir)
            self.bilitools.down_video(video_list, title, start_url, page, save_dir)
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
        self.heards['referer'] = 'https://space.bilibili.com/{}/video'.format(usid)
        while True:
            last_page = self.getUpAllBvide()
            vids = [[i["aid"], i["bvid"]] for i in self.tasks]
            for index, vid in enumerate(vids):
                try:
                    self.bilitools = tools()
                    avid = vid[0]
                    self.start_url = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(avid)
                    html = requests.get(self.start_url, headers={'User-Agent':  get_random_agent()}).json()
                    data = html['data']['pages']
                    self.download_cid(data)
                    time.sleep(random.random() + random.randint(3, 10))
                except:

                    print("download {} failed".format(avid))
                print(data)
            if not last_page:
                tarDir(os.path.join(self.save_path, str(usid)) + '.tar.gz', self.save_path)
                break


if __name__ == "__main__":
    save_path = "bili_results/"
    # 1080p:80;720p:64;480p:32;360p:16
    quality = 32
    main = bilidowload_upid(save_path, quality)
    # 添加up主id list
    usid_list = [98627270]
    if len(usid_list) == 0:
        usid = input('请输入您要下载的B站up猪的id:')
        main.download_usid(str(usid))
    else:
        for usid in usid_list:
            main.download_usid(str(usid))
