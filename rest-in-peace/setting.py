KEYSPACE_NAME = 'chat'
INDEX_NAME = 'chat'

import os
REDIS_HOST = 'localhost'
CASSANDRA_HOSTS = ['localhost:9042']
ES_HOSTS = ['localhost']
if os.environ['ENVIRONMENT'] == 'production':
    # REDIS_HOST = 'localhost'
    # CASSANDRA_HOSTS = ['localhost:9042']
    # ES_HOSTS = ['localhost']
    pass
