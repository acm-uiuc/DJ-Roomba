"""
Handles joy stick communication to roomba
"""

from argparse import ArgumentParser
from .joystick import Joystick

HOST = 'localhost'
DEVICE = '/dev/input/event13'
ROOMBA_QUEUE = 'r.drive'
TURRET_QUEUE = 't.drive'

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

@app.register('btn_west', TURRET_QUEUE)
def left(_):
    return ('left',)

@app.register('btn_east', TURRET_QUEUE)
def right(_):
    return ('right',)

@app.register('btn_north', TURRET_QUEUE)
def up(_):
    return ('up',)

@app.register('btn_south', TURRET_QUEUE)
def down(_):
    return ('down',)

@app.register('btn_tr2', TURRET_QUEUE)
def fire(_):
    return ('fire',)
    

def main():
    """Entry point for the joystick daemon"""
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', required=True)
    parser.add_argument('--host', default=HOST)
    parser.add_argument('--device', '-d', default=None)
    args = parser.parse_args()
    app.run(args.broker, args.device, args.config)
