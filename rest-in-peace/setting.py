KEYSPACE_NAME = 'chat'
INDEX_NAME = 'chat'

import os
REDIS_HOST = 'localhost'
CASSANDRA_HOSTS = ['localhost']
ES_HOSTS = ['localhost']
if 'ENVIRONMENT' in os.environ and os.environ['ENVIRONMENT'] == 'production':
    REDIS_HOST = 'redis-master'
    CASSANDRA_HOSTS = ['cassandra-0.cassandra.default.svc.cluster.local', 'cassandra-1.cassandra.default.svc.cluster.local', 'cassandra-2.cassandra.default.svc.cluster.local']
    ES_HOSTS = ['elasticsearch-master']
