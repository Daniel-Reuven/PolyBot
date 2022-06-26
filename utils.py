import logging
import os
import boto3
from botocore.exceptions import ClientError
from youtube_dl import YoutubeDL
from time import sleep


def search_download_youtube_video(video_name, num_results, s3_bucket_name):
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
                # check local for file
                if not (os.path.isfile(f'{ydl.prepare_filename(video)}')):
                    dlflag = True
                # check aws s3 bucket for file
                # if not (check_s3_file(ydl.prepare_filename(video), s3_bucket_name)):
                #     video_url = video.get("url", None)
                #     ydl.extract_info(video_url, download=True)
                #     upload_file(ydl.prepare_filename(video), s3_bucket_name)
            sleep(1)
            # Download files if required and return the list of files, will not be relevant if above code will work, only need to return the list of filenames/urls from s3
            if dlflag is True:
                dlvideos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=True)['entries']
                # for video in dlvideos:
                #     if not (check_s3_file(ydl.prepare_filename(video), s3_bucket_name)):
                #         upload_file(ydl.prepare_filename(video), s3_bucket_name)
                return [ydl.prepare_filename(video) for video in dlvideos]
            else:
                # for video in videos:
                #     s3 = boto3.client('s3')
                #     s3.download_file(s3_bucket_name, ydl.prepare_filename(video), ydl.prepare_filename(video))
                return [ydl.prepare_filename(video) for video in videos]
    except:
        return "Error, Server error has occurred"


def check_s3_file(key_filename, s3_bucket_name):
    objs = list(s3_bucket_name.objects.filter(Prefix=key_filename))
    if len(objs) > 0 and objs[0].key == key_filename:
        return True
    else:
        return False


def upload_file(key_filename, bucket, object_name=None):
    # Upload the file
    s3_client = boto3.client('s3')
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(key_filename)
    try:
        response = s3_client.upload_file(key_filename, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
