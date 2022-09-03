import os
import re
import asyncio
from aiohttp import ClientSession

class ProgressCounter(asyncio.Lock):
    __currentProgress__:int
    __previousPercent__:int
    __totalProgress__:int
    
    def __init__(self,total:int) -> None:
        super().__init__()
        self.__currentProgress__=0
        self.__previousPercent__=0
        self.__totalProgress__=total

    def CurrentProgress(self) -> float:
        return (self.__currentProgress__/self.__totalProgress__)

    def AddProgress(self,size:int) -> None:
        self.__currentProgress__+=size
        percent=int(self.CurrentProgress()*100)
        if percent>self.__previousPercent__:
            print(f'Progress: {percent}%')
        self.__previousPercent__=percent

class MultiLinkDownload:

    # *structors:
    async def __fulfill_queue__(self, links:list[str]) -> None:
        totalLength=0
        for link in links:
            response=await self.__session__.head(link)
            totalLength+=int(response.headers['Content-Length'])
            await self.__links__.put(link)
        self.Progress=ProgressCounter(totalLength)

    def __init__(self,*,name:str,links:list[str],session:ClientSession) -> None:
        self.Name=name
        self.__links__=asyncio.Queue()
        self.__session__=session
        self.__loop__=asyncio.get_event_loop()
        
        self.__loop__.run_until_complete(self.__loop__.create_task(self.__fulfill_queue__(links)))

    def __del__(self) -> None:
        del self.Name
        del self.__links__
        self.__loop__.run_until_complete(self.__session__.close())
        del self.__session__

    # Technical methods:
    async def __download_stream__(self):
        while not self.__links__.empty():
            link=await self.__links__.get()
            # fileName=os.path.basename(link)
            fileName=re.search('hls-\d+p-?\w*\.ts',link)[0]

            r=await self.__session__.get(link)
            with open(f'Downloads\\{fileName}','wb') as resultFile:
                async for chunk in r.content.iter_chunked(4096):
                    await self.Progress.acquire()
                    self.Progress.AddProgress(len(chunk))
                    resultFile.write(chunk)
                    self.Progress.release()

            # Older way:
            # r=await self.__session__.get(link)
            # with open(f'Downloads\\{fileName}','wb') as resultFile:
            #     print(f'In contextmanager for {fileName}')
            #     resultFile.write(r.content)
            #     print(f'Finished contextmanager for {fileName}')

    def __downdload_task__(self) -> asyncio.Task:
        loop=asyncio.get_event_loop()
        return loop.create_task(self.__download_stream__())

    # Public methods:
    def Fetch(self,*,parallelDownloads:int) -> None:
        loop=asyncio.get_event_loop()
        downloads=[self.__downdload_task__() for _ in range(parallelDownloads)]
        loop.run_until_complete(asyncio.wait(downloads))
