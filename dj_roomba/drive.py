"""
"""

import json
import logging

import amqp

HOST = 'localhost'
DECODE_ERROR_MSG = 'Value Error: likely due to ill formed json:\n{msg}'
FORMAT_ERROR_MSG = "Type Error: likely b.c. msg wasn\'t a json array\n{msg}"

class Driver(object):
    """
    """
    def __init__(self, *, callback:"*args -> IO ()", host:str=HOST, queue:str):
        """
        """
        self.host, self.queue = host, queue
        self._callback = callback

    def callback(self, msg:amqp.Message) -> "IO ()":
        """
        """
        try:
            args = json.loads(msg.body)
            self._callback(*args)
        except TypeError:
            logging.info(FORMAT_ERROR_MSG)
        except ValueError:
            logging.info(DECODE_ERROR_MSG.format(msg))


    def drive(self) -> "IO ()":
        """
        """
        connection = amqp.Connection(self.host)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_consume(queue=self.queue, callback=self.callback)

        while channel.callbacks:
            channel.wait()
