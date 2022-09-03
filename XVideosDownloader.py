from XVideo import XVideo
from Downloader import Downloader

# link='https://www.xvideos.com/video32367025/_dategirl.top_'
link='https://www.xvideos.com/video30380011/_'
# link = 'https://www.xvideos.com/video7388507/_'
# link='https://www.xvideos.com/video49521087/_._'

video=XVideo(URL=link)
video.Retrieve()

downloader = Downloader()
downloader.Download(name=video.title,links=video.Resolutions()[-1][1])