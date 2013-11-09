def noop(state, val):
    return ('foo', state)

def drive_straight(state, val):
    state = ROBOT('straight', -val*300, state.mode)
    return ('drive_straight', state.speed), state

def turn(state, val):
    state = ROBOT('turn', -val*300, state.mode)
    return ('drive', state.speed, 0), state

def control(state, val):
    return ('control',), ROBOT(0, 0, START)
