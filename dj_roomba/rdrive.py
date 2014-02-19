from roomba.controllers import BluetoothController, PyRobotControllerError
from roomba.roomba import Create, RoombaError
from .drive import Driver

DRIVE_QUEUE = 'drive'
ROOMBA_ADDRESS = '00:0A:3A:2E:C9:BB'

def callback(roomba:Create, cmd:str, *args) -> "IO ()":
    try:
        getattr(roomba, cmd)(*args)  # Tell roomba what to do
    except AttributeError:
        pass  # should log bad msg
    except PyRobotControllerError:
        pass
    except RoombaError:
        pass

def main(address=ROOMBA_ADDRESS, queue=DRIVE_QUEUE) -> "IO ()":
    roomba = Create(BluetoothController(address))
    roomba.control()
    Driver(callback=lambda cmd, *args: getattr(roomba, cmd)(*args), 
          queue=queue).drive()
