"""
Handles joy stick communication to amqp broker
"""
import json
from functools import wraps

import amqp
import evdev

class Joystick(object):
    """Used to register and read evdev events for mapping to amqp queues."""
    def __init__(self):
        self.event_map = {}
        self.queues = set()

    def register(self, code:int, queue:str):
        """Register's event to be mapped by function on a queue"""
        @wraps
        def decorator(func):
            self.queues.add(queue)
            self.event_map[code] = func
            return func
        return decorator

    def messages(self, events:[evdev.events], config:dict) -> [amqp.Message]:
        """Maps the events from evdev events to amp msgs based on event_map"""
        codes_and_values = ((config[str(event.code)], event.value) for event
                            in events if event.code in self.event_map)
        for code, value in codes_and_values:
            command = events[code](value)
            yield amqp.Message(json.dumps(command)), self.event_map[code]

    def run(self, broker:str, device:str, config_path:str) -> 'IO ()':
        """Executes monitoring loop"""
        connection = amqp.Connection(broker)
        channel = connection.channel()
        for queue in self.queues:
            channel.queue_declare(queue=queue)

        device = evdev.device.InputDevice(device)
        with open(config_path, 'r') as handle:
            config = json.load(handle)

        for msg, queue in self.messages(device.read_loop(), config):
            channel.basic_publish(msg, routing_key=queue)
