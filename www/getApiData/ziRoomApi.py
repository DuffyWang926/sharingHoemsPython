from getApiData.ziRoomData import getZiRoomData


def getZiRoomApiData(key):
    # keyword=urllib.parse.quote(key.encode('gb2312'))
    # url = 'http://www.ziroom.com/z/?qwd={key}' 
    result = []
    resultZiRoom = getZiRoomData(key)

    result.append(resultZiRoom)
    
    return result

