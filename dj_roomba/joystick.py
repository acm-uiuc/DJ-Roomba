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

def messages(events, config):
    state = ROBOT(0, START)
    for code, value in events:
        command, state = EVENT_TO_ACTION[code](state, value)
        yield amqp.Message(json.dumps(command))
    

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

    events = ((config[str(event.code)], event.value) for event
              in device.read_loop())
    events = (event for event in events if event[0] in EVENT_TO_ACTION)
    for msg in messages(events, config):
        print(msg)
        channel.basic_publish(msg, routing_key=drive_queue)

