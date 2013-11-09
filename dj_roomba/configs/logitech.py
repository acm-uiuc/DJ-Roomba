from ..commands import noop, control, turn, drive_straight

# Buttons/Triggers 0:off 1:on
# Axis: -1: left, 0: neutral, 1: right
EVENT_TO_ACTION = {
    304: noop, # 1
    305: noop, # 2
    306: noop, # 3
    307: noop, # 4
    308: noop, # LB (5)
    309: noop, # RB (6)
    310: noop, # LT (7)
    311: noop, # RT (8)
    312: noop, # SELECT (9)
    313: control, # SELECT (10)
    16: turn,  # x
    17: drive_straight,  # y
}
