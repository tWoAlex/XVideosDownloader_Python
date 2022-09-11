import os
import re

from XVideo import XVideo
from Downloader import Downloader

def __clean_download_folder__() -> None:
    # print(os.listdir('Downloads'))
    
    os.chdir('Downloads')
    print(filesInDownloadFolder:=os.listdir())
    for file in filesInDownloadFolder:
        os.remove(file)

    pass

def __concatenate_downloaded_parts__(fileName:str) -> None:
    parts=sorted(os.listdir('Downloads'))
    fileName+=re.search('\.\w+',parts[0])[0]
    print(fileName)
    
    with open('Downloads\\'+fileName,'wb') as resultFile:
        for part in parts:
            resultFile.write(open('Downloads\\'+part,'rb').read())
    pass

if __name__=='__main__':
    
    links=['https://www.xvideos.com/video30380011/_',
        'https://www.xvideos.com/video32367025/_dategirl.top_',
        'https://www.xvideos.com/video7388507/_',
        'https://www.xvideos.com/video49521087/_._']

    video=XVideo(URL=links[0])
    video.Retrieve()

    downloader = Downloader()
    downloader.Download(name=video.title,links=video.Resolutions()[-1][1])

    # __clean_download_folder__()
    # __concatenate_downloaded_parts__(video.title)