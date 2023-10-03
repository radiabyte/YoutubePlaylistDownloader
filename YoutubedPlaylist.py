import os
import pytube
from pytube import Playlist
from pytube import YouTube
import re
from pathvalidate import sanitize_filename


currentloc=str(os.getcwd())
req=currentloc+'\Downloaded'
if os.path.exists(req)==False:
    os.system('md Downloaded')

videos=[]

play=input('Enter the link of your youtube playlist: ')



def file_check(url):
    yt=YouTube(url)
    tit=yt.title
    nam=sanitize_filename(tit+'.mp3')
    filedir=req+r'/'+nam
    return os.path.isfile(filedir)

    
def get_urls(play_url):
    global videos
    play=Playlist(play_url)
    for url in play.video_urls:
        videos.append(str(url))
    play=None


def extract_variable_value(stream_metadata, variable_name):
    match=re.search(rf'{variable_name}="(.+?)" ',stream_metadata)
    if match:
        return match.group(1)
    else:
        return None


def get_best_res(list_audio):
    a=[]
    b=[]
    for items in list_audio:
        x=int((str(extract_variable_value(str(items),'abr'))).strip('kbps'))
        y=str(extract_variable_value(str(items),'itag'))
        a.append(x)
        b.append(y)
    mydic={}
    for i in range(0,len(a)):
        mydic[a[i]]=b[i]
    mykeys=list(mydic.keys())
    mykeys.sort()
    sorteddic={i:mydic[i] for i in mykeys}
    sorteddickeylist=list(sorteddic.keys())
    sorteddicvaluelist=list(sorteddic.values())
    stuff=len(sorteddickeylist)-1
    return sorteddicvaluelist[stuff]

while True:
    try:
        get_urls(play)
        for url in videos:
            if file_check(url)==False:
                yt=YouTube(url)
                list_audio=yt.streams.filter(only_audio=True)
                idno=get_best_res(list_audio)
                stream=yt.streams.get_by_itag(idno)
                pastname=yt.title+'.mp3'
                name=sanitize_filename(pastname)
                filedir=req+r'/'+name
                print('Downloading', name)
                stream.download(filename=name,output_path=req)
                print('Done')
        print(r'Done for this playlist. Press ctrl+c to stop or let it run to keep looking for videos')
    except KeyboardInterrupt:
        print('Exiting. Bye')
        break

