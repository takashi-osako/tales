'''
Created on May 18, 2013

@author: dorisip
'''
from kombu import Connection, Queue
from kombu.entity import Exchange, PERSISTENT_DELIVERY_MODE
from cloudy_tales.queue import client
import json

default_exchange = Exchange('default', 'direct', durable=True)
# routing key denotes the name of the queue
pdf_queue = Queue('pdf', routing_key='pdf', exchange=default_exchange, durable=True)


def publish(msg, conn_url='amqp://guest@localhost//'):
    '''
    Publishes a mesage
    '''
# Don't use KOMBU - remove this code later
#    with Connection(conn_url) as conn:
#        with conn.Producer() as producer:
#            # declare means make sure pdf queue is declared so that the msg can be delivered
#            producer.publish(msg, declare=[pdf_queue, callback_queue], exchange=default_exchange, routing_key='pdf', delivery_mode=PERSISTENT_DELIVERY_MODE, reply_to=uuid)
    return client.publish(json.dumps(msg))
