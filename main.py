from __future__ import unicode_literals
import youtube_dl
import sys


def main(args):
    url = args[0]
    index = url.find('.json')
    if index != -1 and url.find('master') != -1:
        newurl = url[0:index] + '.mpd' + url[index + len('.json')::]
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([newurl])
    else:
        print('URL is not correct !')
        exit()
    
    

if __name__ == "__main__":
    if len(sys.argv) > 1 and len(sys.argv) < 3 :
        main(sys.argv[1:])
    else:
        print('Input not specified OR extra arguments passed')
        exit()
