import asyncio
from requests_html import AsyncHTMLSession

class SingleLinkDownload:
    async def __GetResponse__(self):
        response=await self.__session__.get(self.link,stream=True)
        self.__response__=response
        self.size=int(response.headers.get('content-length'))

    def __init__(self, *, link:str, session:AsyncHTMLSession, eventLoop:asyncio.AbstractEventLoop) -> None:
        if not isinstance(link,str):
            raise TypeError('Link must be string')
        self.link=link
        self.fileName=os.path.basename(link)
        print(f'Creation of {self.fileName} started')
        self.__eventLoop__=eventLoop
        self.__session__=session
        eventLoop.run_until_complete(eventLoop.create_task(self.__getResponse__()))
        print(f'Creation of {self.fileName} finished')

    async def __RetrieveContent__(self):
        with open(self.fileName,'wb') as downloadResult:
            for part in self.__response__.iter_content(chunk_size=4096):
                downloadResult.write(part)

    def Retrieve(self):
        self.__eventLoop__.run_until_complete(self.__eventLoop__.create_task(self.__RetrieveContent__()))

    def __del__(self) -> None:
        pass

class MultiLinkDownload:

    # *structors:
    async def __fulfill_queue__(self, links:list[str]) -> None:
        for link in links:
            await self.__links__.put(link)

    def __init__(self,*,name:str,links:list[str],session:AsyncHTMLSession()) -> None:
        self.Name=name
        self.__links__=asyncio.Queue()
        self.__session__=session
        
        loop=asyncio.get_event_loop()
        loop.run_until_complete(loop.create_task(self.__fulfill_queue__(links)))
        
    def __del__(self) -> None:
        self.__session__.close()

    # Technical methods:
    async def __download_stream__(self):
        while not self.__links__.empty():
            link=await self.__links__.get()
            fileName=os.path.basename(link)
            r=await self.__session__.get(link)
            with open(f'Downloads\\{fileName}','wb') as resultFile:
                print(f'In contextmanager for {fileName}')
                resultFile.write(r.content)
                print(f'Finished contextmanager for {fileName}')

    def __downdload_task__(self) -> asyncio.Task:
        loop=asyncio.get_event_loop()
        return loop.create_task(self.__download_stream__())

    # Public methods:
    def Fetch(self,*,parallelDownloads:int) -> None:
        loop=asyncio.get_event_loop()
        downloads=[self.__downdload_task__() for _ in range(parallelDownloads)]
        loop.run_until_complete(asyncio.wait(downloads))