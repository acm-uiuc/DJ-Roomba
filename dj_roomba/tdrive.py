from functools import partial
import usb.core
import amqp
import json
import logging
import time

HOST = 'localhost'
DRIVE_QUEUE = 't.drive'

CMD_BYTE = {
    'up': 0x02,
    'down': 0x01,
    'left': 0x04,
    'right': 0x08,
    'stop': 0x20,
    'fire': 0x10,
}

def send_cmd(dev, cmd):
    dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, CMD_BYTE[cmd], 0x00, 0x00, 0x00,
                                         0x00, 0x00, 0x00])
    if cmd == "fire":
        time.sleep(3)
    else:
        time.sleep(0.2)

    dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, CMD_BYTE['stop'], 0x00, 0x00, 0x00,
                                         0x00, 0x00, 0x00])


def drive(send_cmd, message):
    print(message.body)
    try:
        msg = json.loads(message.body)
        try:
            cmd, _ = msg[0], msg[1:]
            print(cmd)
            print(send_cmd)
            send_cmd(cmd)
        except AttributeError:
            print('here3')
            pass  # should log bad msg
        except TypeError:
            print('here4')
            pass  # this means message wasn't subscriptable'
    except ValueError:
        print("here2")
        #This means the json failed to decode correctly
        #Should be logged
        pass


def main():
    dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
    if dev is None:
        raise ValueError('Launcher not found.')
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    dev.set_configuration()
    

    connection = amqp.Connection(HOST)
    channel = connection.channel()
    channel.queue_declare(queue=DRIVE_QUEUE)
    _drive = partial(drive, partial(send_cmd, dev))
    channel.basic_consume(queue=DRIVE_QUEUE, callback=_drive)

    while channel.callbacks:
        print('here')
        channel.wait()
if __name__ == '__main__':
    main()
