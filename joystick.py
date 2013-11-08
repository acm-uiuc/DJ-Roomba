import json
from collections import namedtuple

import amqp
import evdev

HOST = 'localhost'
DRIVE_QUEUE = 'drive'
DEVICE = '/dev/input/event13'
ROBOT = namedtuple('Robot', 'drive speed mode')
START, SAFE, FULL = range(3)

NOP = lambda state, val: (('foo'), state)
def drive_straight(state, val):
    state = ROBOT('straight', -val*300, state.mode)
    return ('drive_straight', state.speed), state

def turn(state, val):
    state = ROBOT('turn', -val*300, state.mode)
    return ('drive', state.speed, 0), state

def control(state, val):
    return ('control',), ROBOT(0, 0, START)
    
    
DRIVE_STRAIGHT = lambda state, val: (("drive"), state)

# Buttons/Triggers 0:off 1:on
# Axis: -1: left, 0: neutral, 1: right
EVENT_TO_ACTION = {
    304: NOP, # 1
    305: NOP, # 2
    306: NOP, # 3
    307: NOP, # 4
    308: NOP, # LB (5)
    309: NOP, # RB (6)
    310: NOP, # LT (7)
    311: NOP, # RT (8)
    312: NOP, # SELECT (9)
    313: control, # SELECT (10)
    16: turn,  # x
    17: drive_straight,  # y
}

def main(host=HOST, drive_queue=DRIVE_QUEUE, device= DEVICE):
    """Creates connection to amqp on HOST to channel DRIVE, """
    connection = amqp.Connection(host)
    channel = connection.channel()
    channel.queue_declare(queue=drive_queue)

    # maybe add controller callibration??
    device = evdev.device.InputDevice(device) # get evdev device

    state = ROBOT(0, 0, START)
    for event in device.read_loop():
        if event.code in EVENT_TO_ACTION.keys():
            command, state = EVENT_TO_ACTION[event.code](state, event.value)
            msg = amqp.Message(json.dumps(command))
            channel.basic_publish(msg, routing_key=drive_queue)


if __name__ == '__main__':
    main()
