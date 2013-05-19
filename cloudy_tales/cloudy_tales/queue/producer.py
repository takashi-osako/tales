'''
Created on May 18, 2013

@author: dorisip
'''
from kombu import Connection, Queue
from kombu.entity import Exchange


default_exchange = Exchange("default", "direct", durable=True)
pdf_queue = Queue('pdf', routing_key='pdf', exchange=default_exchange)


def publish(msg, conn_url='amqp://guest@localhost//'):
    '''
    Publishes a mesage
    '''
    with Connection(conn_url) as conn:
        with conn.Producer() as producer:
            producer.publish(msg, declare=[pdf_queue], exchange=default_exchange, routing_key='pdf')
