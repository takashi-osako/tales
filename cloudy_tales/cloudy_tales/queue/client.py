'''
Created on May 25, 2013

@author: dorisip
'''
import pika
import uuid


class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.connection.add_timeout(15, self.on_timeout)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def on_timeout(self):
        self.response = ""

    def call(self, msg):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='pdf',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id,),
                                   body=msg)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


def publish(msg):
    rpc = RpcClient()
    return rpc.call(msg)