'''
Created on May 25, 2013

@author: dorisip
'''
import pika
import uuid
import json
from cloudy_tales.exceptions.exceptions import RPCTimeout
from zope import interface, component


def create_queue_connection(host='localhost'):
    '''
    Register mongoClient in zope
    '''
    rpc_client = RpcClient(host=host)
    component.provideUtility(rpc_client, IRpcClient)


class IRpcClient(interface.Interface):
    def close_connection(self):
        pass

    def on_response(self):
        pass

    def on_timeout(self):
        pass

    def publish(self):
        pass


class RpcClient():
    interface.implements(IRpcClient)
    '''
    Client that makes RPC call to rabbitmq to get pdf file content
    '''
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # unnamed queue, queue is exclusive per connection
        result = self.channel.queue_declare(durable=False, exclusive=True, auto_delete=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        self.connection.close()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def on_timeout(self):
        raise RPCTimeout()
    
    def get_timeout_id(self):
        return self.connection.add_timeout(15, self.on_timeout)

    def remove_timeout(self, timeout_id):
        self.connection.remove_timeout(timeout_id)

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
        rpc = component.getUtility(IRpcClient)
        timeout_id = rpc.get_timeout_id()
        results = rpc.publish(json.dumps(msg))
    except RPCTimeout:
        results = None
    finally:
        rpc.remove_timeout(timeout_id)
    return results
