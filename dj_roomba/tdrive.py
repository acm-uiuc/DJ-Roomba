"""Module for controlling the storm launcher turret"""
import time
from functools import partial

import usb.core
from .drive import Driver

DRIVE_QUEUE = 't.drive'
REQUEST_TYPE, REQUEST = 0x21, 0x09
VENDOR, PRODUCT = 0x2123, 0x1010
CMD_BYTE = {'down': 0x01, 'up': 0x02, 'left': 0x04, 'right': 0x08,
           'stop': 0x20, 'fire': 0x10}

def make_data(cmd:str) -> [int]:
    """Builds data list required by ctrl_transfer to turret"""
    return [0x02, CMD_BYTE[cmd]] + 6*[0]

def send_cmd(ctrl_transfer:'[int] -> IO ()' , cmd:'str') -> 'IO ()':
    """Sends the command given to the turret over usb"""
    ctrl_transfer(data_or_wLength=make_data(cmd))
    time.sleep(3 if cmd == "fire" else 0.2)
    ctrl_transfer(data_or_wLength=make_data('stop'))

def main(queue:str=DRIVE_QUEUE) -> 'IO ()':
    """Reads from the t.drive queue for commands for the turret."""
    dev = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)
    if dev is None:
        raise ValueError('Launcher not found.')
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    dev.set_configuration()

    func = partial(send_cmd, partial(dev.ctrl_transfer, REQUEST_TYPE, REQUEST))
    Driver(callback=func, queue=queue).drive()
