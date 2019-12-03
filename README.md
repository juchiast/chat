# chat

https://paper.dropbox.com/doc/CHAT-tPo5eMiyeC4HhRyqojC2E

# Run code

Run database:
```
./db
```

Reset database and run:
```
./db --clear
```

Run REST server:
```
cd rest-in-peace
./run_dev.bash
```

Insert messages:
```
python3 raw_data/setup_data.py
```

# Ref

- https://blog.discordapp.com/how-discord-indexes-billions-of-messages-e3d5e9be866f
- https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
- https://kubernetes.io/docs/tutorials/stateless-application/guestbook/
- https://kubernetes.io/docs/tutorials/stateful-application/cassandra/
- https://medium.com/faun/deploying-a-cassandra-cluster-in-kubernetes-on-ibm-cloud-59e840c1a9b7
