'''
Created on Jun 9, 2013

@author: tosako
'''
import pika
import uuid
import json


class PdfClient():

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.connection.add_timeout(15, self.timedout)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.corr_id = None
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if props.correlation_id == self.corr_id:
            self.response = body

    def call(self, msg):
        self.corr_id = str(uuid.uuid4())
        self.response = None
        self.channel.basic_publish(exchange='', routing_key='pdf', properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id), body=(json.dumps(msg)))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def timedout(self):
        self.response = 'Failed to generate requested PDF'
