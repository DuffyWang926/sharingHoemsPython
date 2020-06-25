import aiomysql
import asyncio
import logging

logobj = logging.getLogger('mysql')

class Pmysql:
    __connection = None

    def __init__(self):
        self.cursor = None
        self.connection = None

    @staticmethod
    async def getconnection():
        if Pmysql.__connection == None:
            conn = await aiomysql.connect(
                host='127.0.0.1',
                port=3306,
                user='wefRoot',
                password='wefRoot',
                db='test',
                )
            if conn:
                Pmysql.__connection = conn
                return conn
            else:
                raise("connect to mysql error ")
        else:
            return Pmysql.__connection

    async def query(self,query,args=None):
        self.cursor = await self.connection.cursor()
        await self.cursor.execute(query,args)
        r = await self.cursor.fetchall()
        await self.cursor.close()
        return r

async def test():
    conn = await Pmysql.getconnection()
    mysqlobj.connection = conn
    await conn.ping()
    r = await mysqlobj.query("select * from users")
    for i in r:
        print(i)
    conn.close()

if __name__ == '__main__':
    mysqlobj = Pmysql()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()