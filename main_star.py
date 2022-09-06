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
from urllib import parse
import numpy as np
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


class bilidowload_search():
    """
    根据搜索进行下载
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
                       'cookie': "buvid3=3AF07C34-32F4-0979-A929-211DBF6B8B0149955infoc; _uuid=7108D9738-3AF10-7E27-4FA7-3310D84D61510750542infoc; buvid4=3A2FB40E-E4CE-ADB5-95CC-B38FDB75BE8E50929-022052711-f/VY5USLPe8r5GBR7g9Alg%3D%3D; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO9216536211653715; is-2022-channel=1; rpdid=|(k|Rll)JYJl0J'uYlJYkuu~m; fingerprint=60fdc3a91a63a9bd329966445052cfc6; buvid_fp_plain=undefined; DedeUserID=11815999; DedeUserID__ckMd5=93f6294bfbd19127; buvid_fp=60fdc3a91a63a9bd329966445052cfc6; b_ut=5; nostalgia_conf=-1; SESSDATA=ee4745c3%2C1670291268%2Cbfd74%2A61; bili_jct=76f935b3f03c725f292cfecec3d7529e; "
                                 "sid=94kl8v74; hit-dyn-v2=1; PVID=1; blackside_state=0; bp_video_offset_11815999=673467373445972000; CURRENT_FNVAL=80; innersign=0; bsource=search_google; b_lsid=C8EF61097_181B21F5775; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_3AF07C34%22%3A%22181B2404FEF%22%2C%22333.999.fp.risk_3AF07C34%22%3A%22181B255856D%22%2C%22333.937.fp.risk_3AF07C34%22%3A%22181A7F7CFB5%22%2C%22333.788.fp.risk_3AF07C34%22%3A%22181A7F7F509%22%2C%22333.337.fp.risk_3AF07C34%22%3A%22181B2407015%22%2C%22888.2421.fp.risk_3AF07C34%22%3A%22181B255BF59%22%2C%22777.5.0.0.fp.risk_3AF07C34%22%3A%22181B255C231%22%7D%7D",
                        'dnt': '1',
                       'origin': 'https://search.bilibili.com',
                       'referer': '', # https://search.bilibili.com/all?vt=52981999&keyword=pyy&from_source=webtop_search&spm_id_from=333.1007
                       'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
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
                       'from_spmid': '333.337',
                       'jsonp': 'jsonp',
                       'platform': 'pc',
                       'highlight': '1',
                       'single_column': '0',
                       'keyword': 'pyy',
                       'preload': 'true',
                       'com2co': 'true'
                       }

        self.url = 'https://api.bilibili.com/x/web-interface/search/all/v2?__refresh__=true&' \
                   '_extra=&context=&page=1&page_size=30&order=&duration=&from_source=&from_spmid=333.337&' \
                   'platform=pc&highlight=1&single_column=0&keyword={}&preload=true&com2co=true'

        self.bilitools = tools()

    def getUpAllBvide(self):
        """
        根据us id获取到当前页的所有video id
        :param usid:
        :return:
        """
        getJson_ = getJson(url=self.url, headers=self.heards, params=self.params)
        if str(getJson_['code']) == "0":
            self.tasks = [j for i in getJson_['data']['result'] if len(list(i["data"])) > 0 for j in i['data']]
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

    def download_usid(self, searchkey):
        """
        下载主函数
        :param usid:
        :return:
        """
        self.heards['user-agent'] = get_random_agent()
        self.params['mid'] = usid
        keyword = parse.quote(searchkey, encoding='utf-8')
        self.heards['referer'] = 'https://search.bilibili.com/all?vt=52981999&keyword={}&from_source=webtop_search&spm_id_from=333.1007'.format(keyword)
        self.url = 'https://api.bilibili.com/x/web-interface/search/all/v2?__refresh__=true&' \
                   '_extra=&context=&page=1&page_size=30&order=&duration=&from_source=&from_spmid=333.337&' \
                   'platform=pc&highlight=1&single_column=0&keyword={}&preload=true&com2co=true'.format(keyword)
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
                # print(data)
            if not last_page:
                # tarDir(os.path.join(self.save_path, str(usid)) + '.tar.gz', self.save_path)
                break

def up_get(path_):
    import os
    import pickle
    dict_ = []
    path_list = [os.path.join(path_, i) for i in os.listdir(path_)]
    for path_i in path_list:
        with open(path_i, 'rb') as f:
            d_i = pickle.load(f)
            for d in d_i.keys():
                dict_.append(d_i[d])
    dict_sort = sorted(dict_, key=lambda i: float(i['fans']), reverse=True)
    dict_sort_dict = {}
    for i in dict_sort: dict_sort_dict[i['upid']] = i
    # print(len(list(dict_.keys())))
    # save_id = []
    return [dict_sort_dict[i]['upid'] for i in list(dict_sort_dict.keys())[:1000]]
    # for name  in list(dict_sort_dict.keys())[:1000]:
    #     di = dict_sort_dict[name]
    #     up_id = di['upid']
    #     upname = di['upname']
    #     fans = di['fans']
    #     vdnums = di['vdnums']
    #     print("粉丝数:{}w,名称:{},视频数:{}".format(fans//10000, upname, vdnums))


if __name__ == "__main__":
    save_path = "bili_results_lee/"
    up_id_path = "../up_id_keys_collect_web/up_pkl"
    quality = 32 # 1080p:80;720p:64;480p:32;360p:16
    main = bilidowload_search(save_path, quality)
    # 添加up主id list
    # usid_list = up_get(up_id_path)
    # np.save("usid_list.npy", usid_list)
    with open("star", "r", encoding="utf-8") as f:
        usid_list = f.readlines()[0]
    usid_list = [i + "+采访" for i in usid_list.split(" ")]
    # usid_list = ["彭于晏+采访"]
    if len(usid_list) == 0:
        usid = input('请输入您要下载搜索的内容:')
        main.download_usid(str(usid))
    else:
        for usid in usid_list:
            main.download_usid(str(usid))
