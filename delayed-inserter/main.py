import asyncio
import aioredis
from async_timeout import timeout
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import elasticsearch 
import json

KEYSPACE_NAME = 'chat'
INDEX_NAME = 'chat'

cluster = Cluster()
session = cluster.connect(KEYSPACE_NAME)
es = elasticsearch.Elasticsearch()

insert_message = session.prepare("insert into messages (id, content, user_name, room_id) values (?,?,?,?)")


def insert_messages(messages):
    if len(messages) == 0:
        return
    batch = BatchStatement()
    bulk = []
    for m in messages:
        batch.add(insert_message.bind((m['id'], m['content'], m['user_name'], m['room_id'])))

        doc = {"index": { "_index": INDEX_NAME }}
        bulk.append(json.dumps(doc))
        bulk.append(json.dumps(m))
    session.execute(batch)
    es.bulk(body="\n".join(bulk))



async def main():
    redis = await aioredis.create_redis_pool('redis://localhost')
    (channel, ) = await redis.subscribe('new_messages')
    
    while True:
        max_delay = 1
        max_count = 500
        messages = []
        try:
            async with timeout(max_delay):
                while len(messages) < max_count:
                    messages.append(await channel.get_json())
        except:
            pass
        finally:
            insert_messages(messages)

    redis.close()
    await redis.wait_closed()


asyncio.run(main())
