create keyspace chat with replication = {'class':'SimpleStrategy','replication_factor':1};
use chat;
create table messages (
    id bigint, 
    content varchar,
    room_id int,
    user_name varchar,
    primary key ((room_id), id))
    with clustering order by (id desc);
