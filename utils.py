import os
from youtube_dl import YoutubeDL
from time import sleep


def search_download_youtube_video(video_name, num_results):
    """
    This function downloads the first num_results search results from YouTube
    :param video_name: string of the video name to search
    :param num_results: integer representing how many videos to download
    :return: list of paths to your downloaded video files
    """
    # Flag to check if file/s exist on server or download is required
    dlflag = False
    # Parameters for youtube_dl use
    ydl = {'noplaylist': 'True', 'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4', 'outtmpl': '/./ytdlAppData/%(id)s.%(ext)s'}
    # Try to download and return list of video/s or error msg
    try:
        with YoutubeDL(ydl) as ydl:
            ydl.cache.remove()
            # 1. get a list of video file names with download=false parameter
            videos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=False)['entries']
            # for each file name in list, check duration limits, then if not exists, mark download required flag(dlflag = True)
            for video in videos:
                if video['duration'] >= 900:
                    return "Error, selected track/s are above predefined duration limit"
                if video['duration'] <= 0.1:
                    return "Error, selected track/s are below predefined duration limit"
                if not (os.path.isfile(f'{ydl.prepare_filename(video)}')):
                    dlflag = True
            sleep(1)
            # Download files if required and return the list of files
            if dlflag is True:
                dlvideos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=True)['entries']
                return [ydl.prepare_filename(video) for video in dlvideos]
            else:
                return [ydl.prepare_filename(video) for video in videos]
    except:
        return "Error, Server error has occurred"
