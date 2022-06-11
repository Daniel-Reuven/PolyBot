import os
from youtube_dl import YoutubeDL


def search_download_youtube_video(video_name, num_results):
    """
    This function downloads the first num_results search results from Youtube
    :param video_name: string of the video name
    :param num_results: integer representing how many videos to download
    :return: list of paths to your downloaded video files
    """
    ydl = {'noplaylist':'True', 'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]'}
    with YoutubeDL(ydl) as ydl:

        # 1. get a list of video file names with download=false
        videos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=False)['entries']
        # for each file name in list, check if exists, if not download.
        for video in videos:
            print(os.getcwd())
            print('filename:')
            print(f'{ydl.prepare_filename(video)}')
            print('does it exist locally')
            print(os.path.isfile(f'{ydl.prepare_filename(video)}'))
            if not (os.path.isfile(f'{ydl.prepare_filename(video)}')):
                videos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=True)['entries']
        # return list either way.
    return [ydl.prepare_filename(video) for video in videos]
