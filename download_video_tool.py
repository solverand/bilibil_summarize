import asyncio
from bilibili_api import video, Credential, HEADERS
import httpx
import os
import json

from config import settings
import imageio_ffmpeg

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

# Load cookies lazily to allow running without file at import time

def _load_cookies() -> dict:
    try:
        with open(settings.cookie_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("cookie/cookie.json 未找到。请先在 cookie 目录下放置有效的登录 Cookie。")
        return {}


async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            async for chunk in resp.aiter_bytes(1024):
                if not chunk:
                    break
                process += len(chunk)
                print(f'下载 {info} {process} / {length}')
                f.write(chunk)


async def download_video(bvid):
    print("download_video:", bvid)
    path = str(settings.video_dir)

    cookies = _load_cookies()
    SESSDATA = cookies.get("SESSDATA", "")
    BILI_JCT = cookies.get("bili_jct", "")
    BUVID3 = cookies.get("sid", "")

    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid=bvid, credential=credential)
    info = await v.get_info()
    print(info.get("duration"))
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()

    # MP4 流下载
    await download_url(streams[0].url, os.path.join(path, "video_temp.m4s"), "视频流")
    await download_url(streams[1].url, os.path.join(path, "audio_temp.m4s"), "音频流")

    # 混流
    output_path = os.path.join(path, f"{bvid}.mp4")
    os.system(f'"{FFMPEG_PATH}" -i {os.path.join(path, "video_temp.m4s")} -i {os.path.join(path, "audio_temp.m4s")} -vcodec copy -acodec copy {output_path}')

    print(f'已下载为：{output_path}')
    return output_path