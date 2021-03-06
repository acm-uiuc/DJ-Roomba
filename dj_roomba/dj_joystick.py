"""
Handles joy stick communication to roomba
"""
import click

from .joystick  import EvdevRabbitJS


HOST = 'localhost'
ROOMBA_QUEUE = 'r.drive'
TURRET_QUEUE = 't.drive'
AUDIO_QUEUE = 'a.drive'

# pylint: disable=C0111, C0103
app = EvdevRabbitJS()

@app.register('BTN_DPAD_DOWN', ROOMBA_QUEUE, weight=-300)
@app.register('BTN_DPAD_UP', ROOMBA_QUEUE, weight=300)
def straight(val):
    return ('drive_straight', val)

@app.register('BTN_DPAD_LEFT', ROOMBA_QUEUE, weight=300)
@app.register('BTN_DPAD_RIGHT', ROOMBA_QUEUE, weight=-300)
def turn(val):
    return ('drive', val, 0)

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

@app.register('FIRE', TURRET_QUEUE)
def fire(val):
    return ('fire', val)

@app.register('NEXT', AUDIO_QUEUE, noop_zero=True)
def next_song(_):
    return ('n', )

@app.register('PAUSE', AUDIO_QUEUE, noop_zero=True)
def pause(_):
    return ('p', )

@app.register('VOL_UP', AUDIO_QUEUE, noop_zero=True)
def vol_up(_):
    return (')', )

@app.register('VOL_DOWN', AUDIO_QUEUE, noop_zero=True)
def vol_down(_):
    return ('(', )
#pylint: enable=C0111, C0103

@click.command()
@click.option('--config', '-c', required=True)
@click.option('--host', '-h', required=True, default=HOST)
@click.option('--device', '-d', required=True)
def main(config, host, device):
    """Entry point for the joystick daemon"""
    app.run(config, host, device)
