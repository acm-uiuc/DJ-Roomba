"""
Handles joy stick communication to roomba
"""

import json
from os.path import join

import amqp
import evdev

from commands import ROBOT, EVENT_TO_ACTION, START

HOST = 'localhost'
DRIVE_QUEUE = 'drive'
DEVICE = '/dev/input/event13'
CONFIG = 'ps4.json'

def main(host=HOST, drive_queue=DRIVE_QUEUE, device=DEVICE):
    """Creates connection to amqp on HOST to channel DRIVE, """
    connection = amqp.Connection(host)
    channel = connection.channel()
    channel.queue_declare(queue=drive_queue)

    # maybe add controller callibration??
    device = evdev.device.InputDevice(device) # get evdev device
    with open(join('configs', CONFIG), 'r') as fp:
        config = json.load(fp)

    state = ROBOT(0, START)
    for event in device.read_loop():
        code, value = config[str(event.code)], event.value
        if code in EVENT_TO_ACTION:
            command, state = EVENT_TO_ACTION[code](state, value)
            msg = amqp.Message(json.dumps(command))
            channel.basic_publish(msg, routing_key=drive_queue)

if __name__ == '__main__':
    main()
