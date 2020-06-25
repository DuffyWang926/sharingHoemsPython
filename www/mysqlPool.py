import logging
import aiomysql
import asyncio

logobj = logging.getLogger('mysql')

class Pmysql:
    def __init__(self):
        self.coon = None
        self.pool = None

    async def initpool(self):
        try:
            logobj.debug("will connect mysql~")
            __pool = await aiomysql.create_pool(
                    minsize=5,
                    maxsize=10,
                    host='127.0.0.1',
                    port=3306,
                    user='wefRoot',
                    password='wefRoot',
                    db='test',
                    autocommit=False)
            return __pool
        except:
            logobj.error('connect error.', exc_info=True)

    async def getCurosr(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor()
        return conn,cur


    async def query(self, query,param=None):
        conn,cur = await self.getCurosr()
        try:
            await cur.execute(query,param)
            return await cur.fetchall()
        except:
            logobj.error('err')
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)

async def test():
    mysqlobj = await getAmysqlobj()
    r = await mysqlobj.query("select * from test")
    for i in r:
        print(i)
    await asyncio.sleep(6)
    r2 = await mysqlobj.query("select * from test where id = (%s)",(1,))
    print(r2)

async def getAmysqlobj():
    mysqlobj = Pmysql()
    pool = await mysqlobj.initpool()
    mysqlobj.pool = pool
    return mysqlobj

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()