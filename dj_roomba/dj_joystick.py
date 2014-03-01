"""
Handles joy stick communication to roomba
"""

from argparse import ArgumentParser
from .joystick import Joystick

HOST = 'localhost'
DEVICE = '/dev/input/event13'
ROOMBA_QUEUE = 'r.drive'

app = Joystick()

@app.register('btn_dpad_up', ROOMBA_QUEUE)
def straight(val):
    return ('drive_straight', -val*300)

@app.register('btn_dpad_right', ROOMBA_QUEUE)
def turn(val):
    return ('drive', -val*300, 0)

@app.register('btn_start', ROOMBA_QUEUE)
def reset(_):
    return ('control',)

def main():
    """Entry point for the joystick daemon"""
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', required=True)
    parser.add_argument('--host', default=HOST)
    parser.add_argument('--device', '-d', default=None)
    args = parser.parse_args()
    app.run(args.broker, args.device, args.config)
