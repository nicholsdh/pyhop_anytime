from pyhop import *

## Operators
def grab(state, dog, biteable):
    if state.holding[dog] is None and state.pos[dog] == state.pos[biteable]:
        state.holding[dog] = biteable
        return state


def drop(state, dog, location):
    if state.holding[dog] is not None:
        state.pos[state.holding[dog]] = location
        state.holding[dog] = None
        return state


def go(state, dog, location):
    if state.pos[dog] != location:
        state.pos[dog] = location
        return state


## Methods
def get_newspaper(state, dog):
    if state.pos['newspaper'] == 'house':
        return TaskList(completed=True)
    else:
        return TaskList([('go', dog, 'driveway'),
                         ('grab', dog, 'newspaper'),
                         ('go', dog, 'house'),
                         ('drop', dog, 'house')])


def make_dog_planner():
    planner = Planner()
    planner.declare_operators(go, grab, drop)
    planner.declare_methods('get_newspaper', get_newspaper)
    return planner


if __name__ == '__main__':
    start_state = State('example1')
    start_state.pos = {'rover': 'house', 'newspaper': 'driveway'}
    start_state.holding = {'rover': None}
    planner = make_dog_planner()
    plan = planner.anyhop(start_state, [('get_newspaper', 'rover')])
    print(plan)