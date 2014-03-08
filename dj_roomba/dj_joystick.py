"""
Handles joy stick communication to roomba
"""

from argparse import ArgumentParser
from .joystick import Joystick

HOST = 'localhost'
DEVICE = '/dev/input/event13'
ROOMBA_QUEUE = 'r.drive'
TURRET_QUEUE = 't.drive'
AUDIO_QUEUE = 'a.drive'

# pylint: disable=C0111, C0103
app = Joystick()

@app.register('BTN_DPAD_DOWN', ROOMBA_QUEUE, weight=-1)
@app.register('BTN_DPAD_UP', ROOMBA_QUEUE, weight=1)
def straight(val):
    return ('drive_straight', val*300)

@app.register('BTN_DPAD_LEFT', ROOMBA_QUEUE, weight=-1)
@app.register('BTN_DPAD_RIGHT', ROOMBA_QUEUE, weight=1)
def turn(val):
    return ('drive', -val*300, 0)

@app.register('BTN_START', ROOMBA_QUEUE)
def reset(_):
    return ('control',)

@app.register('BTN_WEST', TURRET_QUEUE)
def left(val):
    return ('left', val)

@app.register('BTN_EAST', TURRET_QUEUE)
def right(val):
    return ('right', val)

@app.register('BTN_NORTH', TURRET_QUEUE)
def up(val):
    return ('up', val)

@app.register('BTN_SOUTH', TURRET_QUEUE)
def down(val):
    return ('down', val)

@app.register('BTN_TR2', TURRET_QUEUE)
def fire(val):
    return ('fire', val)

@app.register('BTN_A', AUDIO_QUEUE)
def next(val):
    return ('noop',) if val == 0 else ('n', )

#pylint: enable=C0111, C0103

def main():
    """Entry point for the joystick daemon"""
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', required=True)
    parser.add_argument('--host', default=HOST)
    parser.add_argument('--device', '-d', default=None)
    args = parser.parse_args()
    app.run(args.host, args.device, args.config)
