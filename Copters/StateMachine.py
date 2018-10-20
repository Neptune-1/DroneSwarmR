class StateMachine(object):
    TAKING_OFF_STATE = 0
    ANIMATION_STATE = 1
    PAUSE_STATE = 2
    LANDING_STATE = 3

    def __init__(self, start_state=PAUSE_STATE):
        self.state = start_state

    def switch_state(self, new_state):
        self.state = new_state
