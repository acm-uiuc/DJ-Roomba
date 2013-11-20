"""
Handles joy stick communication to roomba
"""

import json
from argparse import ArgumentParser, FileType
from os.path import join, exists, expanduser

import amqp
import evdev

from .commands import ROBOT, EVENT_TO_ACTION, START

HOST = 'localhost'
DRIVE_QUEUE = 'drive'
DEVICE = '/dev/input/event13'

def main(host=HOST, drive_queue=DRIVE_QUEUE, device=DEVICE):
    """Creates connection to amqp on HOST to channel DRIVE, """
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', required=True, type=FileType('r'))
    args = parser.parse_args()
    connection = amqp.Connection(host)
    channel = connection.channel()
    channel.queue_declare(queue=drive_queue)

    # maybe add controller callibration??
    device = evdev.device.InputDevice(device) # get evdev device
    config = json.load(args.config)
    args.config.close()

    state = ROBOT(0, START)
    for event in device.read_loop():
        code, value = config[str(event.code)], event.value
        if code in EVENT_TO_ACTION:
            command, state = EVENT_TO_ACTION[code](state, value)
            msg = amqp.Message(json.dumps(command))
            channel.basic_publish(msg, routing_key=drive_queue)

