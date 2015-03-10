"""Roomba driver subsystem"""

from roomba.controllers import BluetoothController, PyRobotControllerError
from roomba.roomba import Create, RoombaError

from .drive import Driver
import click

DRIVE_QUEUE = 'r.drive'
ROOMBA_ADDRESS = '00:0A:3A:2E:C9:BB'

def callback(roomba:Create, cmd:str, *args) -> "IO ()":
    """Uses introspection on roomba object to get proper command from queue"""
    try:
        getattr(roomba, cmd)(*args)  # Tell roomba what to do
    except AttributeError:
        pass  # should log bad msg
    except PyRobotControllerError:
        pass
    except RoombaError:
        pass

@click.command()
@click.option('--address', default=ROOMBA_ADDRESS)
@click.option('--queue', default=DRIVE_QUEUE)
def main(address:str, queue:str) -> "IO ()":
    """Listens on the r.drive queue for roomba commands"""
    roomba = Create(BluetoothController(address))
    roomba.control()
    Driver(callback=lambda cmd, *args: getattr(roomba, cmd)(*args),
           queue=queue).drive()
