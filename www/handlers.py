from coroweb import get,options,post
from getHtml.ziRoom import getZiRoomHtml 
from getHtml.ziRoom import getZiRoomHtmlSelenium 
import time

@get('/blog/{id}')
def get_blog(id):
    return id

@get('/roomList')
def get_rooms(*args,**kw):
    print(args,'args')
    print(kw,'kw')
    key = kw['key']
    result = []
    # getZiRoomHtml(key)
    result = getZiRoomHtmlSelenium(key)
    return {'data':result}
@options('/logIn')
def get_access():
    return'ss' 

@post('/logIn')
def get_accessd():
    return'ss'   

@options('/roomList/ss')
def get_accessdd():
    return'ss' 