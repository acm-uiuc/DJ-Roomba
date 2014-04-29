"""audio driver subsystem"""

from os.path import exists
from os import environ
from subprocess import check_call
from functools import partial
from .drive import Driver

DRIVE_QUEUE = 'a.drive'
CTL_PATH = '{}/.config/pianobar/ctl'.format(environ['HOME'])
COMMANDS = {'p', 'n', '^', '(', ')'}

def callback(ctl:'file_t', cmd:str) -> "IO ()":
    """writes command to ctl pipe"""
    if cmd not in COMMANDS:
        return
    ctl.write(cmd)
    ctl.flush()

def main(ctl_path:str=CTL_PATH, queue=DRIVE_QUEUE) -> "IO ()":
    """daemon for a.drive queue consumption"""
    if not exists(ctl_path):
        with open('/dev/null', 'w') as null:
            check_call(['pianoctl'], stdout=null)

    with open(ctl_path, 'w') as ctl:
        Driver(callback=partial(callback, ctl), queue=queue).drive()
