import re
from typing import List
from requests_html import HTMLSession
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

        # Technical patterns:
        
            # Part name example: 'hls-1080p-13c650.ts?e=1662139743&l=0&h=cbe980cff92bcf3ce14928e1f19b53e3'
        self.__video_part_pattern__='hls-\d+p-?\w*\.ts\??[=&\w]*'

        # Special:
        self.__steps__={}
        self.__main_page__=None
        self.__resolutions_playlist__=None

    def __del__(self) -> None:
        self.__session__.close()
        del self.__session__

    def __passed__(self, step):
        self.__steps__[step]=True
    def __failed__(self, step):
        self.__steps__[step]=False

    
    # Retrieving video's data steps:

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

    def __get_resolutions_playlist__(self) -> None:
        step='Resolutions playlist'
        try:
            planA = self.__main_page__.html.search(".setVideoHLS('{}')")
            if planA is not None:
                self.__resolutions_playlist__=self.__session__.get(planA[0]).text
                self.__prefix__=os.path.dirname(planA[0])+'/'
            else:
                self.__failed__(step)
            self.__passed__(step)
        except:
            self.__failed__(step)

    def __get_resolution_list__(self) -> None:
        step='Resolution list'
        try:
            #Playlists links' suffixes :
            self.__resolutions__=re.findall('hls-\d+p-?\w*\.m3u8\S*',self.__resolutions_playlist__)

            #Sorted from lowest to highest + links:
            self.__resolutions__=[(int(re.search('\d+p',x)[0][:-1]),self.__prefix__+x) for x in self.__resolutions__]
            self.__resolutions__=sorted(self.__resolutions__)
            resolutions=[]
            for x in self.__resolutions__:
                sub_step=f'Links for {x[0]}'
                try:
                    current_playlist=self.__session__.get(x[1]).text
                    parts=re.findall(self.__video_part_pattern__,current_playlist)
                    parts=[self.__prefix__+x for x in parts]
                    res=(str(x[0])+'p',parts)
                    resolutions.append(res)
                except:
                    self.__failed__(sub_step)
            self.__resolutions__=resolutions

            self.__passed__(step)
        except:
            self.__failed__(step)

    
    # Public methods:

    def Retrieve(self) -> None:
        """Retrieves all data of this video"""
        self.__get_main_page__()
        
        self.__get_title__()
        self.__get_preview__()

        self.__get_resolutions_playlist__()
        self.__get_resolution_list__()

        self.__session__.close()

    def Resolutions(self) -> List:
        """Returns a list of tuples
        Element example: ('720p', *list of links for parts of the video*)"""
        return self.__resolutions__