# bilibili_video_download_upid
bilibili批量下载，用于根据UP主的id下载其所有视频
# 环境配置
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 执行命令
python3 main.py
# 修改参数
save_path = "bili_results/" # 存储地址
quality = 32 # 1080p:80;720p:64;480p:32;360p:16 分辨率
usid_list = [*] # 添加id list, *代表up猪的id
thread_count = 4 # 进程数
# ubuntu，macos运行，请提前配置ffmpeg
pyton3
import imageio
imageio.plugins.ffmpeg.download()

# 新增按照工号执行
python3 main_jbnum.py

# 20221113更新
新增多进程下载：（请保留原始状态缓存的state.txt）
python3 main_jbnum_mult.py

**删除下载进度条
**流下载添加随机agent

