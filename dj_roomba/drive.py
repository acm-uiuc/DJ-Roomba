"""Driver abstraction for the DJ Roomba project"""

import json
import logging

import amqp

HOST = 'localhost'
DECODE_ERROR_MSG = 'Value Error: likely due to ill formed json:\n{msg}'
FORMAT_ERROR_MSG = "Type Error: likely b.c. msg wasn\'t a json array\n{msg}"

class Driver(object):
    """Driver abstraction, register a callback for consuming from a queue"""
    def __init__(self, *, callback:"*args -> IO ()", host:str=HOST, queue:str):
        self.host, self.queue = host, queue
        self._callback = callback

    def callback(self, msg:amqp.Message) -> "IO ()":
        """Wraps user callback for amqp consuming"""
        try:
            args = json.loads(msg.body)
            self._callback(*args)
        except TypeError:
            logging.info(FORMAT_ERROR_MSG)
        except ValueError:
            error_msg = DECODE_ERROR_MSG.format(msg)
            logging.info(error_msg)


    def drive(self) -> "IO ()":
        """Opens connect, channel and consumes until channel closed"""
        connection = amqp.Connection(self.host)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_consume(queue=self.queue, callback=self.callback)

        while channel.callbacks:
            channel.wait()
