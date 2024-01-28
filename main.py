from __future__ import unicode_literals
import sys
import datetime
import youtube_dl
from urllib.parse import urlparse, urlunparse

import ffmpeg
import os

class Video:
    def __init__(self, link=None):
        self.link = link
        self.parsedLink = None
        self.audioCode = None
        self.videoCode = None
        self.splittedPath = None
        self.audioPath = None
        self.videoPath = None
        self.name = None

    def parse_link(self):
        self.parsedLink = urlparse(self.link)
        self.splittedPath = self.parsedLink.path.split('/')

    def get_audio_url(self):
        if self.audioCode is None:
            print("To download the audio file, you need to pass the audio id with '-a' or '--audio'. Example: -a 567fffa")
            return None

        audio_parsed = self.parsedLink
        audio_splitted_path = self.splittedPath

        audio_splitted_path[-2] = 'audio'
        audio_splitted_path[-1] = f'{self.audioCode}.mp4?autoplay=1'

        audio_path = '/'.join(tuple(audio_splitted_path))

        self.audioPath = audio_path

        audio_parsed = audio_parsed._replace(path=audio_path)

        return urlunparse(audio_parsed)

    def get_video_url(self):
        if self.videoCode is None:
            print("To download the video file, you need to pass the video id with '-v' or '--video'. Example: -v 567fffa")
            return None

        video_parsed = self.parsedLink
        video_splitted_path = self.splittedPath

        video_splitted_path[-2] = 'video'
        video_splitted_path[-1] = f'{self.videoCode}.mp4?autoplay=1'

        video_path = '/'.join(tuple(video_splitted_path))

        self.videoPath = video_path

        video_parsed = video_parsed._replace(path=video_path)

        return urlunparse(video_parsed)

    def get_video_name(self):
        if self.videoCode is None:
            print("To set the video name, you need to pass the video id with '-v' or '--video'. Example: -v 567fffa")
            return None

        return f'video_{self.videoCode}.mp4'

    def get_audio_name(self):
        if self.audioCode is None:
            print("To set the audio name, you need to pass the audio id with '-a' or '--audio'. Example: -a 567fffa")
            return None

        return f'audio_{self.audioCode}.mp4'


def merge_audio_and_video(audio_file, video_file, output_file):
    video = ffmpeg.input(video_file)
    audio = ffmpeg.input(audio_file)
    ffmpeg.output(video, audio, output_file).run()


def delete_files(*files):
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {str(e)}")


def main(args):
    video = Video()
    combined_name = None
    for idx, c in enumerate(args):
        if c.startswith('-') or c.startswith('--'):
            if c == '-l':
                video.link = args[idx + 1]
                video.parse_link()
            elif c == '-a' or c == '--audio':
                video.audioCode = args[idx + 1]
            elif c == '-v' or c == '--video':
                video.videoCode = args[idx + 1]
            elif c == '-n' or c == '--name':
                combined_name = args[idx + 1]
            else:
                print('Arguments are not valid')
                exit()

    video_list = {'video': {'url': video.get_video_url(), 'name': video.get_video_name()},
                  'audio': {'url': video.get_audio_url(), 'name': video.get_audio_name()}}

    for vd in video_list:
        ydl_opts = {
            'outtmpl': video_list[vd]['name']
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([video_list[vd]['url']])
            except:
                pass
    
    if combined_name is None:
        output_filename = f'{datetime.datetime.now().strftime("%Y-%m-%d' %H:%M:%S")}_output.mp4'
    else:
        output_filename = combined_name

    merge_audio_and_video(video_list['video']['name'], video_list['audio']['name'], output_filename)
    delete_files(video_list['video']['name'], video_list['audio']['name'])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print('Input not specified')
        exit()
