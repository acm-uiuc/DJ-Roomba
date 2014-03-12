"""
Handles joy stick communication to amqp broker
"""

from json import dumps, load

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

    def messages(self, events:['events'], config:dict) -> [str]:
        """Maps the events from evdev events to amp msgs based on event_map"""
        events2 = ((config[event.code], event.value) for event
                   in events if event.code in config)
        cmd_val_lis = ((self.event_map[code], val) for code, val in events2
                       if code in self.event_map)
        for (cmd, queue, noop_zero), value in cmd_val_lis:
            if noop_zero and value == 0:
                continue
            yield dumps(cmd(value)), queue

    def run(self, config_path:str, source, sink) -> 'IO ()':
        """Executes monitoring loop"""
        with open(config_path, 'r') as handle:
            config = {int(key): val for key, val in load(handle).items()}

        sink(self.messages(source, config))
