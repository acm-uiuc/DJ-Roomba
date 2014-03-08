"""
Handles joy stick communication to amqp broker
"""

import json

import amqp
import evdev

QUEUE_ARGS = {'max-length': 2}

class Joystick(object):
    """Used to register and read evdev events for mapping to amqp queues."""
    def __init__(self):
        self.event_map = {}
        self.queues = set()

    def register(self, code:int, queue:str, *, weight:int=1, noop_zero=False):
        """Register's event to be mapped by function on a queue"""
        # pylint: disable=C0111
        def decorator(func):
            def _decorator(val):
                return func(val*weight)
            self.event_map[code] = (_decorator, queue, noop_zero)
            return _decorator
        self.queues.add(queue)
        return decorator

    def messages(self, events:[evdev.events], config:dict) -> [amqp.Message]:
        """Maps the events from evdev events to amp msgs based on event_map"""
        events2 = ((config[event.code], event.value) for event
                   in events if event.code in config)
        cmd_val_lis = ((self.event_map[code], val) for code, val in events2
                       if code in self.event_map)
        for (cmd, queue, noop_zero), value in cmd_val_lis:
            if noop_zero and value == 0:
                continue
            yield amqp.Message(json.dumps(cmd(value))), queue

    def run(self, broker:str, device:str, config_path:str) -> 'IO ()':
        """Executes monitoring loop"""
        connection = amqp.Connection(broker)
        channel = connection.channel()
        for queue in self.queues:
            channel.queue_declare(queue=queue, arguments=QUEUE_ARGS)

        device = evdev.device.InputDevice(device)
        with open(config_path, 'r') as handle:
            config = {int(key): val for key, val in json.load(handle).items()}

        for msg, queue in self.messages(device.read_loop(), config):
            channel.basic_publish(msg, routing_key=queue)
