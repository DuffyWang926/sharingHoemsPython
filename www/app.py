import logging;logging.basicConfig(level=logging.INFO)
import asyncio,os,json,time

from datetime import datetime
from aiohttp import web
from coroweb import add_routes

async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        return (await handler(request))
    return logger

async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        global resp
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'application/json;charset=UTF-8'
            resp.headers['Location']='http//:8089'
            
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                
               
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                
        if isinstance(r, int) and r >= 100 and r < 600:
            resp = web.Response(text=r)
            
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                resp = web.Response(text=(t+ str(m)))
                
                
        # default:
        # resp = web.Response(body=str(r).encode('utf-8'))
        # resp.content_type = 'text/plain;charset=utf-8'
        # resp.headers['Access-Control-Allow-Origin'] = "*"
        resp.headers['Access-Control-Allow-Origin'] = "*"
        resp.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
        resp.headers['Access-Control-Allow-Methods'] = "PUT,POST,GET,DELETE,OPTIONS"
        # resp.headers['Access-Control-Max-Age'] = '1000'
        # resp.headers['Access-Control-Allow-Headers'] = '*'
        return resp
       
    return response

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    r = web.Response(text=text)
    r.headers['Access-Control-Allow-Origin'] = "*"
    r.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"

    return r

app = web.Application(middlewares=[
        logger_factory, response_factory
    ])


add_routes(app, 'handlers')

# app.add_routes([web.post('/logIn', handle),
# web.options('/logIn', handle),
#                 web.get('/logIn', handle)])

if __name__ == '__main__':
    web.run_app(app)