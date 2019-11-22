import time


def get_timestamp_from_id(id):
        return id >> 31


class MessageIdFactory:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.msg_count = 0

    def generate_message_id(self):
        self.msg_count += 1
        timestamp = int(time.time())
        # 63-bit id:
        # 32-bit timestamp, 8-bit worker's id, 23-bit local counter
        return (timestamp << 31) | (self.worker_id << 23) | (self.msg_count % (1 << 23))
