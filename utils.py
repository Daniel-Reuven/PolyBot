import os
from youtube_dl import YoutubeDL
from time import sleep


def search_download_youtube_video(video_name, num_results):
    """
    This function downloads the first num_results search results from Youtube
    :param video_name: string of the video name
    :param num_results: integer representing how many videos to download
    :return: list of paths to your downloaded video files
    """
    dlflag = False
    ydl = {'noplaylist': 'True', 'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4'}
    with YoutubeDL(ydl) as ydl:
        ydl.cache.remove()

        # 1. get a list of video file names with download=false
        videos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=False)['entries']
        # for each file name in list, check duration limits, then if exists, if not download.
        for video in videos:
            if video['duration'] >= 900:
                return "Error, selected track/s are above defined duration limit"
            if video['duration'] <= 0.1:
                return "Error, selected track/s are below defined duration limit"
            if not (os.path.isfile(f'{ydl.prepare_filename(video)}')):
                dlflag = True
            # return list either way.
        sleep(1)
        if dlflag is True:
            dlvideos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=True)['entries']
            return [ydl.prepare_filename(video) for video in dlvideos]
        else:
            return [ydl.prepare_filename(video) for video in videos]
