from dj_roomba.joystick import Joystick, apply_dict
from unittest import TestCase, main
from unittest.mock import patch, MagicMock

def test_apply_dict():
    mapping = {'a': 1, 'c':2}
    for case, result in [(['a'], [1]), (['a', 'b', 'c'], [1, 2]), (['b'], [])]:
        yield check_dict, list(apply_dict(case, mapping)), result

def check_dict(x, y):
    assert x == y 

class TestDriver(TestCase):
    def setUp(self):
        self.joystick = Joystick()
    
    def test_messages(self):
        pass

    def test_run(self):
        pass

    def test_register(self):
        pass

if __name__ == '__main__':
    main()
