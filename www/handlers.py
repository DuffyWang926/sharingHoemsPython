from coroweb import get,options,post
from getHtml.ziRoom import getZiRoomHtml 
@get('/blog/{id}')
def get_blog(id):
    return id

@get('/roomList/{name}')
def get_rooms(name):
    key='阳光100'
    result = getZiRoomHtml(key)
    return {'data':result}
@options('/logIn')
def get_access():
    return'ss' 

@post('/logIn')
def get_accessd():
    return'ss'   