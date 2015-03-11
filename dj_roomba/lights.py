"""
Module for controlling lights.

Listens on the audio_level.sensor queue
"""

from __future__ import print_function

from subprocess import check_output

import amqp
QUEUE = "audio_level.sensor"

PINS = [60, 30, 31, 48, 3, 2, 15, 14, 66, 67]
BINS = 127 // len(PINS)

def drive_lights(cmd):
    """Call back for controlling lights based on audio levels."""
    val = cmd.body // len(PINS)
    pin_vals = [(pin, 1) for i, pin in enumerate(PINS) if val > BINS*i]

    set_pins(pin_vals)


def set_pins(pin_vals: "[(pin, val)]") -> "IO ()":
    """Set pins to corresponding value."""
    for pin, val in pin_vals:
        echo("/sys/class/gpio/gpio{}/value".format(pin), val)

def echo(val, path):
    "echo val into file"
    return check_output("echo {} > {}".format(val, path))


def setup_gpio() -> "IO ()":
    """Setup pins to control lights."""
    for pin in PINS:
        echo("/sys/class/gpio/export", str(pin))
        echo("/sys/class/gpio/gpio{}/direction".format(pin), "out")
        echo("/sys/class/gpio/gpio{}/value".format(pin), "1")


def main():
    """Main for controlling lights."""
    setup_gpio()

    connection = amqp.Connection("localhost")
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    channel.basic_consume(queue=QUEUE, callback=drive_lights)

    while channel.callbacks:
        channel.wait()

if __name__ == "__main__":
    main()
