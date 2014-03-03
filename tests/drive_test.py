from amqp import Message
from dj_roomba.drive import Driver
from unittest import TestCase, main
from unittest.mock import patch, MagicMock

class TestDriver(TestCase):
    def setUp(self):
        self.driver = Driver(callback=MagicMock(), host='host', queue='queue')

    def test_init(self):
        self.assertEqual(self.driver.host, 'host')
        self.assertEqual(self.driver.queue, 'queue')

    def test_callback(self):
        msg = Message('["msg"]')
        self.assertEqual(self.driver.callback(msg), None)
        self.driver._callback.assert_called_with('msg')
    
    @patch('dj_roomba.drive.amqp')
    def test_drive(self, amqp):
        channel = amqp.Connection.return_value.channel.return_value
        channel.callbacks = False
        self.assertEqual(self.driver.drive(), None)
        
if __name__ == '__main__':
    main()
