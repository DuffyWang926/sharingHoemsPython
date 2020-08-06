from getApiData.ziRoomData import getZiRoomData
from getApiData.eggShellData import getEggShellData
import asyncio

async def getZiRoomApiData(key):
    result = []
    resultZiRoom = []
    resultEggShell = []
    resultZiRoom = await getZiRoomData(key)
    resultEggShell = await getEggShellData(key)
    result.extend(resultZiRoom)
    result.extend(resultEggShell)
    
    return result


