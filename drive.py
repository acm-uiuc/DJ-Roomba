from functools import partial
from roomba.controllers import BluetoothController, PyRobotControllerError
from roomba.roomba import Create, RoombaError
import amqp
import json

HOST = 'localhost'
DRIVE_QUEUE = 'drive'

def drive(roomba, message):
    try:
        msg = json.loads(message.body)
        try:
            cmd, args = msg[0], msg[1:]
            print(cmd, args)
            getattr(roomba, cmd)(*args)  # Tell roomba what to do
        except AttributeError:
            pass  # should log bad msg
        except TypeError:
            pass  # this means message wasn't subscriptable'
        except PyRobotControllerError:
            pass
        except RoombaError:
            pass
    except ValueError:
        """This means the json failed to decode correctly
        Should be logged"""


def main():
    roomba = Create(BluetoothController('00:0A:3A:2E:C9:BB'))
    roomba.control()
    connection = amqp.Connection(HOST)
    channel = connection.channel()
    channel.queue_declare(queue=DRIVE_QUEUE)
    channel.basic_consume(queue=DRIVE_QUEUE, callback=partial(drive, roomba))

    while channel.callbacks:
        channel.wait()
    
if __name__ == '__main__':
    main()
