import time
import msgpack

from kafka import KafkaConsumer, KafkaProducer
import yaml
import json

with open(r'D:\Work\automation\kafka_conf.yaml', 'r') as f:
    conf = yaml.load(f.read(), Loader=yaml.SafeLoader)
    ka_conf = conf['kafka']
    consumer_conf = conf['consumer']


class KafkaReceive(object):
    def __init__(self, topics: list, **kwargs):
        self.consumer = KafkaConsumer(**ka_conf, **consumer_conf, **kwargs,
                                      value_deserializer=lambda m: json.loads(m.decode()))
        self.consumer.subscribe(topics=topics)
        # 指定topic和partition
        # self.consumer.assign([TopicPartition(topic='encryption', partition=1)])
        # 打印包含的topic
        # print(self.consumer.topics())

    def msg_receive(self):
        print('开始消费')
        index = 0
        while True:
            msg = self.consumer.poll(timeout_ms=5)
            index += 1
            print('--------poll index is %s----------' % index)
            if msg:
                for value in msg.values():
                    print(len(value))
                    print(value[0].topic)
                    print(value[0].timestamp)
                    time_array = time.localtime(value[0].timestamp)
                    send_time = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
                    print(send_time)
            time.sleep(30)


class KafkaSend(object):
    def __init__(self, **kwargs):
        self.producer = KafkaProducer(**ka_conf, **kwargs, value_serializer=msgpack.dumps)

    def msg_send(self, topic, **kwargs):
        future = self.producer.send(topic, **kwargs)
        result = future.get(timeout=10)
        print(result)


if __name__ == '__main__':
    to = ['encryption', 'encrypted', 'decryption']
    recv = KafkaReceive(to)
    recv.msg_receive()

    # with open(r'D:\Work\automation\data.json', 'r') as f:
    #     v = f.read()
    # send = KafkaSend()
    # send.msg_send(topic='encryption', value=v)
