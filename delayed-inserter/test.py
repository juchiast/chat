import redis
import json

N = 5000

r = redis.Redis()
for i in range(N):
    m = {
        'id': i,
        'content': str(i),
        'user_name': str(i),
        'room_id': 1,
    }
    r.publish("new_messages", json.dumps(m))
    print(i, end='\r')
