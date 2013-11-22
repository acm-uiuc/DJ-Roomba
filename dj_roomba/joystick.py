"""
Handles joy stick communication to roomba
"""

import json
from argparse import ArgumentParser, FileType

import amqp
import evdev

from .commands import ROBOT, EVENT_TO_ACTION, START

HOST = 'localhost'
DRIVE_QUEUE = 'drive'
DEVICE = '/dev/input/event13'

def messages(events):
    state = ROBOT(0, START)
    for code, value in events:
        command, state = EVENT_TO_ACTION[code](state, value)
        yield amqp.Message(json.dumps(command))

def main():
    """Creates connection to amqp on HOST to channel DRIVE, """
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', required=True, type=FileType('r'))
    parser.add_argument('--host', '-h', default=HOST)
    parser.add_argument('--queue', '-q', default=DRIVE_QUEUE)
    parser.add_argument('--device', '-d', default=None)
    args = parser.parse_args()

    connection = amqp.Connection(args.host)
    channel = connection.channel()
    channel.queue_declare(queue=args.queue)

    # maybe add controller callibration??
    if args.device is None:
        args.device = DEVICE
    device = evdev.device.InputDevice(args.device) # get evdev device
    config = json.load(args.config)
    args.config.close()

    events = ((config[str(event.code)], event.value) for event
              in device.read_loop())
    events = (event for event in events if event[0] in EVENT_TO_ACTION)
    for msg in messages(events):
        print(msg)
        channel.basic_publish(msg, routing_key=args.queue)
