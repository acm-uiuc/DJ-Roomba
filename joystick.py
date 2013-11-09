"""
Handles joy stick communication to roomba
"""

import imp
import json
from os.path import join
from collections import namedtuple

import amqp
import evdev

HOST = 'localhost'
DRIVE_QUEUE = 'drive'
DEVICE = '/dev/input/event13'
ROBOT = namedtuple('Robot', 'drive speed mode')
START, SAFE, FULL = range(3)
CONFIG = 'controller.cfg'

def main(host=HOST, drive_queue=DRIVE_QUEUE, device=DEVICE):
    """Creates connection to amqp on HOST to channel DRIVE, """
    connection = amqp.Connection(host)
    channel = connection.channel()
    channel.queue_declare(queue=drive_queue)

    # maybe add controller callibration??
    device = evdev.device.InputDevice(device) # get evdev device
    config = imp.load_source(join('configs', CONFIG), CONFIG)

    state = ROBOT(0, 0, START)
    for event in device.read_loop():
        code, value = event.code, event.value
        if code in config.EVENT_TO_ACTION.keys():
            command, state = config.EVENT_TO_ACTION[event.code](state, value)
            msg = amqp.Message(json.dumps(command))
            channel.basic_publish(msg, routing_key=drive_queue)

if __name__ == '__main__':
    main()
