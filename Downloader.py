import os
import asyncio
import aiohttp
from requests_html import AsyncHTMLSession
from DownloadTypes import MultiLinkDownload

class Downloader:
    def __init__(self) -> None:
        self.__session__=AsyncHTMLSession()

    def __del__(self) -> None:
        loop=asyncio.get_event_loop()
        loop.run_until_complete(loop.create_task(self.__session__.close()))
    
    def Download(self,*,name:str,links:list[str]):
        path='Downloads'
        if not os.path.exists(path): os.path.os.mkdir(path)
        myfile=MultiLinkDownload(name=name,links=links,session=self.__session__)
        myfile.Fetch(parallelDownloads=3)
            

# def DownloadMaxResolution(self) -> None:
    #     maxResM3U8=self.__session__.get(self.__resolutions__[-1][1])
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