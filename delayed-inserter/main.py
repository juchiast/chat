import asyncio
import aioredis
from async_timeout import timeout
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import elasticsearch 
import json
import websockets
import time

import setting

cluster = Cluster(setting.CASSANDRA_HOSTS)
session = cluster.connect(setting.KEYSPACE_NAME)
es = elasticsearch.Elasticsearch(setting.ES_HOSTS)

insert_message = session.prepare("insert into messages (id, content, user_name, room_id) values (?,?,?,?)")


class WsStates:
    def __init__(self):
        self.users = dict()

    def enter_room(self, room, user):
        if room not in self.users:
            self.users[room] = []
        self.users[room].append(user)

    async def broadcast(self, room):
        if room not in self.users:
            return
        async def try_send(user):
            try:
                await user.send('{}')
            except:
                return False
            return True
        users = self.users[room]
        if len(users) == 0:
            return
        succeeds = await asyncio.wait([try_send(user) for user in users])
        self.users[room] = []
        for user, succeed in zip(users, succeeds):
            if succeed:
                self.users[room].append(user)
            

ws_states = WsStates()

async def handler(ws, path):
    greeting = json.loads(await ws.recv())
    if 'room_id' not in greeting:
        return
    room = int(greeting['room_id'])
    ws_states.enter_room(room, ws)
    async for message in ws:
        pass

def rewrite_timestamp(time, now):
    time = time % (1 << 31)
    time = time | (int(now) << 31)
    return time

def insert_messages(messages):
    if len(messages) == 0:
        return None
    batch = BatchStatement()
    bulk = []
    rooms = set()
    now = time.time()
    for m in messages:
        rooms.add(m['room_id'])
        m['id'] = rewrite_timestamp(m['id'], now)
        batch.add(insert_message.bind((m['id'], m['content'], m['user_name'], m['room_id'])))
        doc = {"index": { "_index": setting.INDEX_NAME }}
        bulk.append(json.dumps(doc))
        bulk.append(json.dumps(m))
    session.execute(batch)
    es.bulk(body="\n".join(bulk))
    return rooms


async def main():
    await websockets.serve(handler, "0.0.0.0", 8081)
    redis = await aioredis.create_redis_pool(setting.REDIS_HOST)
    (channel, ) = await redis.subscribe('new_messages')
    
    while True:
        max_delay = 1
        max_count = 50
        messages = []
        try:
            async with timeout(max_delay):
                while len(messages) < max_count:
                    messages.append(await channel.get_json())
        except:
            pass
        finally:
            rooms = insert_messages(messages)
            if rooms != None:
                await asyncio.wait([ws_states.broadcast(room) for room in rooms])

    redis.close()
    await redis.wait_closed()


asyncio.run(main())
