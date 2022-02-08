import unittest

import pyhop
from pyhop import TaskList


def go(state, entity, start, end):
    if state.loc[entity] == start and end in state.connected[start] and end not in state.visited[entity]:
        state.loc[entity] = end
        state.visited[entity].append(end)
        return state


def turn_on_lights(state, entity, loc):
    if state.loc[entity] == loc and loc not in state.lights_on:
        state.lights_on.append(loc)
        return state


def find_route(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    elif end in state.connected[start]:
        return TaskList([('go', entity, start, end)])
    else:
        return TaskList([[('go', entity, start, neighbor), ('find_route', entity, neighbor, end)]
                         for neighbor in state.connected[start]])


def light_bringer(state, entity, dark_place):
    if dark_place in state.lights_on:
        return TaskList(completed=True)
    else:
        return TaskList([('find_route', entity, state.loc[entity], dark_place), ('turn_on_lights', entity, dark_place)])


def make_travel_planner():
    planner = pyhop.Planner()
    planner.declare_operators(go, turn_on_lights)
    planner.declare_methods('find_route', find_route)
    planner.declare_methods('light_bringer', light_bringer)
    return planner


def setup_state(title, people, connections):
    state = pyhop.State(title)
    state.visited = {person: [] for (person,location) in people}
    state.loc = {person: location for (person,location) in people}
    state.lights_on = []
    state.connected = {}
    for (loc1, loc2) in connections:
        if loc1 not in state.connected:
            state.connected[loc1] = []
        if loc2 not in state.connected:
            state.connected[loc2] = []
        state.connected[loc1].append(loc2)
        state.connected[loc2].append(loc1)
    return state


class Test(unittest.TestCase):
    def test1(self):
        state = setup_state('state',
                            [('robot', 'mcrey312')],
                            [('mcrey312', 'hallway'), ('mcrey312', 'mcrey314'), ('mcrey314', 'hallway'), ('lounge', 'hallway'), ('copyroom', 'lounge')])
        print(state)
        planner = make_travel_planner()
        plans = planner.anyhop(state, [('find_route', 'robot', 'mcrey312', 'copyroom')], verbose=4)
        print(plans)
        plans = [plan for (plan, time) in plans]
        self.assertEqual(plans, [[('go', 'robot', 'mcrey312', 'mcrey314'), ('go', 'robot', 'mcrey314', 'hallway'), ('go', 'robot', 'hallway', 'lounge'), ('go', 'robot', 'lounge', 'copyroom')], [('go', 'robot', 'mcrey312', 'hallway'), ('go', 'robot', 'hallway', 'lounge'), ('go', 'robot', 'lounge', 'copyroom')]])
        plan = planner.pyhop(state, [('find_route', 'robot', 'mcrey312', 'no-room')])
        self.assertEqual(plan, None)


if __name__ == "__main__":
    unittest.main()
