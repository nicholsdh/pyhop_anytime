from pyhop import *


def hand_on_table(state, hand):
    if state.pos[hand] != 'table':
        state.pos[hand] = 'table'
        return state


def lift_hand(state, hand):
    if state.pos[hand] != 'lifted':
        state.pos[hand] = 'lifted'
        return state


def raise_glass(state, hand):
    if state.pos[hand] == 'table':
        return TaskList([('lift_hand', hand)])
    else:
        return TaskList(completed=True)


def make_hand_planner():
    planner = Planner()
    planner.declare_operators(hand_on_table, lift_hand)
    planner.declare_methods('raise_glass', raise_glass)
    return planner


planner = make_hand_planner()
state = State('demo1')
state.pos = {'left': 'table', 'right': 'table'}

plan = planner.pyhop(state, [('raise_glass', 'left')], verbose=3)
print(plan)