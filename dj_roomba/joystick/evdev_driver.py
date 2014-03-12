"""AMQP and EVDEV joystick support"""

from functools import partial

from .joystick import Joystick
import amqp
import evdev

QUEUE_ARGS = {'max-length': 2}

def sink(channel:amqp.Channel, source:[('msg', 'queue')]) -> "IO ()":
    """Amqp sink"""
    for msg, queue in ((amqp.Message(msg), queue) for msg, queue in source):
        channel.basic_publish(msg, routing_key=queue)

class EvdevRabbitJS(Joystick):
    """Provides convenience wrapper around Joystick using evdev and RabbitMQ"""
    def run(self, config_path:str, broker:str, device:str) -> "IO ()":
        connection = amqp.Connection(broker)
        channel = connection.channel()
        for queue in self.queues:
            channel.queue_declare(queue=queue, arguments=QUEUE_ARGS)

        device = evdev.device.InputDevice(device)
        super().run(config_path, device.read_loop(), partial(sink, channel))
