import orm
import asyncio
from models import User, Blog, Comment

async def test(loop):
    await orm.create_pool(loop = loop,user='wefRoot', password='wefRoot', database='test')

    u = User(name='Test', email='treedsd@example.com', passwd='1234567890', image='about:blank')

    await u.save()
    await orm.conn_close()

if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test(loop))
        print('Test finished.')

        # loop.close()

# for x in test(loop):
#     pass