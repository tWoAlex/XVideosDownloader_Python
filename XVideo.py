import re
from requests_html import HTMLSession
import requests

class XVideo:
    URL = None

    def __init__(self, *, URL: str) -> None:
        self.URL = URL

        self.Title = None
        self.__steps__ = None
        self.__prefix__ = None
        self.__suffix__ = None
        self.__HLS__ = None
        self.__Resolutions__= None
        self.__ResolutionsPlaylists__= None

        self.__session__ = HTMLSession()
        self.__steps__ = {}

    def __del__(self) -> None:
        self.__session__.close()
        del self.__session__
        print(self.Title, 'destroyed')

    def __passed__(self, step: str):
        self.__steps__[step] = True

    def __failed__(self, step: str):
        self.__steps__[step] = False

    def __getMainPage__(self) -> None:
        step='MainPage'
        self.__failed__(step)
        try:
            self.__MainPage__ = self.__session__.get(self.URL)
            self.__passed__(step)
        except:
            pass

    def __getTitle__(self) -> None:
        step='Title'
        self.__passed__(step)
        planA = self.__MainPage__.html.search('"video_title":"{}"')
        planB = self.__MainPage__.html.search(".setVideoTitle('{}')")
        if planA is not None:
            self.Title = planA[0]
        elif planB is not None:
            self.Title = planB[0]
        else:
            self.__failed__(step)

    def __getHLS__(self) -> None:
        step='HLS'
        self.__failed__(step)
        try:
            planA = self.__MainPage__.html.search(".setVideoHLS('{}')")
            if planA is not None:
                hlsURL = planA[0]
                self.__HLS__ = self.__session__.get(hlsURL)
                with open('HLS.m3u8', 'w') as hlsfile:
                    hlsfile.write(self.__HLS__.text)
            else:
                return
            self.__prefix__ = hlsURL[:hlsURL.rindex('hls.m3u8')]
            self.__suffix__ = hlsURL[hlsURL.rindex('.m3u8')+5:]
            self.__passed__(step)
        except:
            pass

    def __getResolutionList__(self) -> None:
        step='ResolutionList'
        self.__failed__(step)
        try:
            #Links for playlists:
            self.__Resolutions__=re.findall('hls-\d+p-?\w*\.m3u8',self.__HLS__.text)

            #(Vertical Resolution as int (for sorting),Link for playlist) List:
            self.__Resolutions__=[(int(re.search('\d+p',x)[0][:-1]),self.__prefix__+x) for x in self.__Resolutions__]
            self.__Resolutions__=sorted(self.__Resolutions__)
            
            self.__passed__(step)
        except:
            print('Step except')
            pass
    
    def DownloadMaxResolution(self) -> None:
        maxResM3U8=self.__session__.get(self.__Resolutions__[-1][1])
        fileLinks=[self.__prefix__+x for x in re.findall('hls-\d+p-?\w*\.ts',maxResM3U8.text)]
        print(f'First file:\n{fileLinks[0]}')
        with open('result.ts','wb') as result:
            result.write(self.__session__.get(fileLinks[0]).content)
            response=requests.get(fileLinks[0],stream=True)
            total_length=response.headers.get('content-length')
            if total_length is None:
                result.write(response.content)
            else:
                progress=0
                total_length=int(total_length)
                for part in response.iter_content(chunk_size=4096):
                    progress+=len(part)
                    result.write(part)
                    print(f'\rProgress: {progress*100//total_length}%')

        # print(f'Total length:{total_length}')


    def Retrieve(self) -> None:
        self.__getMainPage__()
        self.__getTitle__()
        self.__getHLS__()
        self.__getResolutionList__()