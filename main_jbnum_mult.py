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
import pickle
import multiprocessing
from utils import *
from tools import *
from upid_get_and_up import *

class bilidowload_upid():
    """
    根据up猪id进行批量下载
    """
    def __init__(self,save_path = "bili_results/", quality = 32, thread_count=2):
        self.save_path = save_path  # 视频下载存放位置
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        self.tasks = []
        self.process = thread_count
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
        save_dir = os.path.join(self.save_path, self.params['mid'])
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        # 创建线程池
        title_list = []
        for item in cid_list:
            cid = str(item['cid'])
            # print("cid", cid)
            title = item['part']
            title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
            title = str(cid) + "_" + title
            title_list.append(title)
            page = str(item['page'])
            start_url = self.start_url + "/?p=" + page
            video_list = get_play_list(start_url, cid, self.quality)
            start_time = time.time()
            # title_list.append([video_list, title, start_url, page, save_dir])
            self.bilitools.down_video(video_list, title, start_url, page, save_dir)
        # 最后合并视频
        # print(title_list)
        # self.bilitools.combine_video(title_list, save_dir)

        end_time = time.time()  # 结束时间
        print('下载总耗时%.2f秒,约%.2f分钟' % (end_time - start_time, int(end_time - start_time) / 60))

    def download_usid(self, usid):
        """
        下载主函数
        :param usid:
        :return:
        """
        # 剩余磁盘大小判断，小于5G停下
        capacity = get_free_space_mb(self.save_path)
        if capacity < 5:
            print("------剩余空间告急，小于5G，请及时传输数据和清理磁盘--------")
            return False

        self.heards['user-agent'] = get_random_agent()
        self.params['mid'] = usid
        self.heards['referer'] = 'https://space.bilibili.com/{}/video'.format(usid)
        if os.path.isfile("data_dict.pkl"):
            with open("data_dict.pkl", 'rb') as f:
                data_dict = pickle.load(f)
        else:
            data_dict = {}
            while True:
                # 循环翻页补货所有页面的vid
                next_page = self.getUpAllBvide()
                vids = [[i["aid"], i["bvid"]] for i in self.tasks]
                for index, vid in enumerate(vids):
                    print(index, "--------", vid)
                    try:
                        self.bilitools = tools()
                        avid = vid[0]
                        self.start_url = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(avid)
                        html = requests.get(self.start_url, headers={'User-Agent':  get_random_agent()}).json()
                        data = html['data']['pages']
                        data_dict[avid] = data
                        # self.download_cid(data)
                        time.sleep(random.random() + random.randint(1, 4))
                    except:
                        print("get vid data {} failed".format(vid[0]))
                    # break
                if not next_page:
                    break
            # 保存缓存文件dict
            with open("data_dict.pkl", 'wb') as f:
                pickle.dump(data_dict, f, pickle.HIGHEST_PROTOCOL)
        print("总共获取到{}个视频，准备下载".format(len(data_dict)))
        # 开始下载所有vid
        data_list = []
        for data in data_dict.values():
            # self.download_cid(data)
            p = multiprocessing.Process(target=self.download_cid, args=(data,))
            data_list.append(p)
            if len(data_list) % self.process == 0 and len(data_list) > 0:
                [x.start() for x in data_list]
                [p.join() for p in data_list]
                data_list = []
                time.sleep(random.random() + random.randint(10, 20))
        # 如果存在余量没有下载完
        if len(data_list) > 0:
            [x.start() for x in data_list]
            [p.join() for p in data_list]
        # 删除缓存文件
        os.remove("data_dict.pkl")
        # zip_file(os.path.join(self.save_path,usid))
        return True

def download_with_jbnum(save_path, quality, usid, thread_count):
    """
    根据工号下载
    :param save_path:
    :param quality:
    :param usid:
    :return:
    """
    # 创建视频下载类
    main = bilidowload_upid(save_path, quality, thread_count)
    # 创建id获取类
    up_main = up_id_get(usid)
    # 本地初始化校验
    if not os.path.isfile("state.txt"):
        state = 0
        nid = False
    else:
        # 本地下载状态校验
        with open("state.txt", "r", encoding="utf-8") as f:
            f_line = f.readlines()
            if len(f_line) == 0:
                nid = 0
                state = 0
            else:
                f_line = f_line[0]
                nid, state = f_line.strip().split(",")
                state = int(state)
    if not nid or state:
        # 如果本地结束或者未开始，获取新的up主id
        nid = up_main.get_new_id()
        state = 0
    if not nid:
        print("-----库里没有数据了------")
        return False
    # J记录状态
    with open("state.txt", "w", encoding="utf-8") as f:
        f.write(",".join([str(nid), str(state)]))
    # 下载主函数
    end = main.download_usid(str(nid))
    if not end:
        return False
    with open("state.txt", "w", encoding="utf-8") as f:
        f.write(",".join([str(nid), str(1)]))
    # 更新服务器状态
    up_main.up_id_statu(nid)
    return True


if __name__ == "__main__":
    save_path = "../bili_results"
    # save_path = "bili_results"
    # 1080p:80;720p:64;480p:32;360p:16
    quality = 64 #
    thread_count = 4 #进程数
    # usid = "X6024"
    usid = input('请输入您的工号:')
    while True:
        statue = download_with_jbnum(save_path, quality, usid, thread_count)
        if not statue:
            break

