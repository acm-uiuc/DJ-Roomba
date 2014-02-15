from functools import partial
import usb.core
import amqp
import json
import logging

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

def drive(send_cmd, message):
    try:
        msg = json.loads(message.body)
        try:
            cmd, _ = msg[0], msg[1:]
            send_cmd(cmd)
        except AttributeError:
            pass  # should log bad msg
        except TypeError:
            pass  # this means message wasn't subscriptable'
    except ValueError:
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
    channel.basic_consume(queue=DRIVE_QUEUE, callback=partial(drive, dev))

    while channel.callbacks:
        channel.wait()
