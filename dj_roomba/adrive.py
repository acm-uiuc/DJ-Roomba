from os.path import exists
from os import environ
from subprocess import check_call
from functools import partial
from .drive import Driver

DRIVE_QUEUE = 'audio.drive'
CTL_PATH = '{}/.config/pianobar/ctl'.format(environ['HOME'])
COMMANDS = {'p', 'n', '^', '(', ')'}

def callback(ctl:'filet', cmd:str) -> "IO ()":
    if cmd not in COMMANDS:
        return
    ctl.write(cmd)
    ctl.flush()

def main(ctl_path:str=CTL_PATH, queue=DRIVE_QUEUE) -> "IO ()":
    if not exists(ctl_path):
        with open('/dev/null', 'w') as null:
            check_call(['pianoctl'], stdout=null)
    ctl = open(ctl_path, 'w')
    Driver(callback=partial(callback, ctl), queue=queue).drive()
    ctl.close()
