"""
Handles joy stick communication to amqp broker
"""
import json
from functools import wraps
from itertools import tee

import amqp
import evdev

def dict_filter(lis, dic):
    return (dic[elem] for elem in lis if elem in dic)

class Joystick(object):
    """Used to register and read evdev events for mapping to amqp queues."""
    def __init__(self):
        self.event_map = {}
        self.queues = set()

    def register(self, code:int, queue:str, *, weight:int=1):
        """Register's event to be mapped by function on a queue"""
        def decorator(func):
            def _decorator(val):
                return func(val*weight)
            self.event_map[code] = (_decorator, queue)
            return _decorator
        self.queues.add(queue)
        return decorator
        
    def messages(self, events:[evdev.events], config:dict) -> [amqp.Message]:
        """Maps the events from evdev events to amp msgs based on event_map"""
        events_v, events_e = tee(events)        
        values = (event.value for event in events_v)
        codes = dict_filter((str(event.code) for event in events_e), config)
        cmd_queue_lis = dict_filter(codes, self.event_map)
        print(self.event_map)

        for (cmd, queue), value in zip(cmd_queue_lis, values):
            print(cmd(value))
            yield amqp.Message(json.dumps(cmd(value))), queue

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
