import re
from requests_html import HTMLSession
import requests
import os

class XVideo:
    def __init__(self, *, URL: str) -> None:
        # Known:
        self.URL = URL

        # Unknown:
        self.title= None
        self.preview_name = None
        self.preview_bytes = None

        # Unknown (technical):
        self.__prefix__ = None
        self.__resolutions__= None
        self.__session__ = HTMLSession()

        # Special:
        self.__steps__={}
        self.__main_page__=None
        self.__resolutionsplaylist__=None

    def __del__(self) -> None:
        self.__session__.close()
        del self.__session__
        print(self.title, 'destroyed')

    def __passed__(self, step):
        self.__steps__[step]=True
    def __failed__(self, step):
        self.__steps__[step]=False



    

    

    # def __getHLS__(self) -> None:
    #     step='HLS'
    #     self.__failed__(step)
    #     try:
    #         planA = self.__main_page__.html.search(".setVideoHLS('{}')")
    #         if planA is not None:
    #             hlsURL = planA[0]
    #             self.__HLS__ = self.__session__.get(hlsURL)
    #             with open('HLS.m3u8', 'w') as hlsfile:
    #                 hlsfile.write(self.__HLS__.text)
    #         else:
    #             return
    #         self.__prefix__ = hlsURL[:hlsURL.rindex('hls.m3u8')]
    #         self.__suffix__ = hlsURL[hlsURL.rindex('.m3u8')+5:]
    #         self.__passed__(step)
    #     except:
    #         pass

    # def __getResolutionList__(self) -> None:
    #     step='ResolutionList'
    #     self.__failed__(step)
    #     try:
    #         #Links for playlists:
    #         self.__Resolutions__=re.findall('hls-\d+p-?\w*\.m3u8',self.__HLS__.text)

    #         #(Vertical Resolution as int (for sorting),Link for playlist) List:
    #         self.__Resolutions__=[(int(re.search('\d+p',x)[0][:-1]),self.__prefix__+x) for x in self.__Resolutions__]
    #         self.__Resolutions__=sorted(self.__Resolutions__)
            
    #         self.__passed__(step)
    #     except:
    #         print('Step except')
    #         pass
    
    # def DownloadMaxResolution(self) -> None:
    #     maxResM3U8=self.__session__.get(self.__Resolutions__[-1][1])
    #     fileLinks=[self.__prefix__+x for x in re.findall('hls-\d+p-?\w*\.ts',maxResM3U8.text)]
    #     print(f'First file:\n{fileLinks[0]}')
    #     with open('result.ts','wb') as result:
    #         result.write(self.__session__.get(fileLinks[0]).content)
    #         response=requests.get(fileLinks[0],stream=True)
    #         total_length=response.headers.get('content-length')
    #         if total_length is None:
    #             result.write(response.content)
    #         else:
    #             progress=0
    #             total_length=int(total_length)
    #             for part in response.iter_content(chunk_size=4096):
    #                 progress+=len(part)
    #                 result.write(part)
    #                 print(f'\rProgress: {progress*100//total_length}%')

    def __get_main_page__(self) -> None:
        step='Main page'
        try:
            self.__main_page__= self.__session__.get(self.URL)
            self.__passed__(step)
        except:
            self.__failed__(step)
    
    def __get_title__(self) -> None:
        step='Title'
        self.__passed__(step)
        
        planA = self.__main_page__.html.search('"video_title":"{}"')
        planB = self.__main_page__.html.search(".setVideoTitle('{}')")
        
        if planA is not None:
            self.title = planA[0]
        elif planB is not None:
            self.title = planB[0]
        else:
            self.__failed__(step)

    def __get_preview__(self) -> None:
        step='Preview'

        planA = self.__main_page__.html.search('<meta property="og:image" content="{}" />')
        if planA is not None:
            self.preview_name=os.path.basename(planA[0])
            self.preview_bytes=self.__session__.get(planA[0]).content
            self.__passed__(step)
        else:
            self.__failed__(step)

    # Public methods:

    def Retrieve(self) -> None:
        self.__get_main_page__()
        self.__get_title__()
        self.__get_preview__()
        self.__session__.close()