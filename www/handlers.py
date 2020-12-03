from coroweb import get,options,post
from getApiData.ziRoomApi import getZiRoomApiData 
from getHtml.ziRoom import getZiRoomHtmlSelenium 
import time
import asyncio

@get('/date')
async def get_date(*args,**kw):
    result = []
    return {'data':result}
