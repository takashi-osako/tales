'''
Created on May 25, 2013

@author: dorisip
'''
import pika
import uuid
import json
from cloudy_tales.exceptions.exceptions import RPCTimeout


class RpcClient(object):
    '''
    Client that makes RPC call to rabbitmq to get pdf file content
    '''
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.connection.add_timeout(15, self.on_timeout)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def close_connection(self):
        self.connection.close()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def on_timeout(self):
        raise RPCTimeout()

    def publish(self, msg):
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
    '''
    Publish the message to queue and blocks until results are returned or timeout has occurrred
    '''
    try:
        rpc = RpcClient()
        results = rpc.publish(json.dumps(msg))
    except RPCTimeout:
        results = None
    finally:
        rpc.close_connection()
    return results
