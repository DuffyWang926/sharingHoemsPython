from getApiData.ziRoomData import getZiRoomData
from getApiData.eggShellData import getEggShellData


def getZiRoomApiData(key):
    # keyword=urllib.parse.quote(key.encode('gb2312'))
    # url = 'http://www.ziroom.com/z/?qwd={key}' 
    result = []
    # resultZiRoom = getZiRoomData(key)
    resultEggShell = getEggShellData(key)

    # result.append(resultZiRoom)
    result.append(resultEggShell)
    
    return result

