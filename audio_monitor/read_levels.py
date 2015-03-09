from __future__ import print_function

import amqp
QUEUE = "audio_level.sensor"

PINS = [60, 30, 31, 48, 3, 2, 15, 14, 66, 67]
BINS = 127 // len(PINS)

def drive_lights(cmd):
    val = cmd.body // len(PINS)
    pin_vals = [(pin, 1) for i, pin in enumerate(PINS) if val > BINS*i]
    
    set_pins(pin_vals)


def set_pins(pin_vals):
    for pin, val in pin_vals:
        with open("/sys/class/gpio/gpio{}/value".format(pin)) as value:
            value.write(str(val))


def setup_gpio():
    for pin in PINS:
        with open("/sys/class/gpio/export") as export:
            export.write(str(pin))
        with open("/sys/class/gpio/gpio{}/direction".format(pin)) as direction:
            value.write("out")
        with open("/sys/class/gpio/gpio{}/value".format(pin)) as value:
            value.write("1")


def main():
    setup_gpio()

    connection = amqp.Connection("localhost")
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    channel.basic_consume(queue=QUEUE, callback=drive_lights)

    while channel.callbacks:
        channel.wait()

if __name__ == "__main__":
    main()
