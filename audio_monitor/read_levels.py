import amqp
QUEUE = "audio_level.sensor"

def drive_lights(cmd):
    print(cmd.body)

def main():
    connection = amqp.Connection("localhost")
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    channel.basic_consume(queue=QUEUE, callback=drive_lights)

    while channel.callbacks:
        channel.wait()

if __name__ == "__main__":
    main()
