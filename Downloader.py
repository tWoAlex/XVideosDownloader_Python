import os
import asyncio
from aiohttp import ClientSession
from requests_html import AsyncHTMLSession
from DownloadTypes import MultiLinkDownload

class Downloader:
    def __init__(self) -> None:
        self.__loop__=asyncio.get_event_loop()
        self.__session__=ClientSession()

    def __del__(self) -> None:
        self.__loop__.run_until_complete(self.__loop__.create_task(self.__session__.close()))
    
    def Download(self,*,name:str,links:list[str]):
        path='Downloads'
        if not os.path.exists(path): os.path.os.mkdir(path)
        myfile=MultiLinkDownload(name=name,links=links,session=self.__session__)
        myfile.Fetch(parallelDownloads=3)