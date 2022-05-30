# bilibili_video_download_upid
bilibili批量下载，用于根据UP主的id下载其所有视频
# 环境配置
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 修改存储地址 main.py 136
save_path = "bili_results/"
# 修改下载分辨率 main.py 138， 
quality = 32 #1080p:80;720p:64;480p:32;360p:16
# 在main 154行 中添加id list, *代表up猪的id.或者直接执行main.py
usid_list = [*]

# 执行命令
python3 main.py

# ubuntu，macos运行，请提前配置ffmpeg
pyton3
import imageio
imageio.plugins.ffmpeg.download()

