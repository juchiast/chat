import aiohttp
import random
import json
import asyncio

host = "https://chat.vietcodes.com/api"
rooms = [1, 2, 3, 4, 5, 6]
users = ['lisa', 'kenny', 'voldy']
size = 600000

async def main():
    f = open("./sentences.txt", 'r')
    session = aiohttp.ClientSession()
    futures = []
    for i in range(size):
        text = f.readline()
        room = random.choice(rooms)
        user = random.choice(users)
        url = f"{host}/{room}/"
        data = {
            'user_name': user,
            'message': text,
        }
        await session.post(url, json=data)
        if i % 80 == 0:
            words = text.split(" ")
            query = random.choice(words)
            search_url = f"{url}search/"
            data = {
                'query': query,
            }
            await session.post(search_url, json=data)

    f.close()


asyncio.run(main())
