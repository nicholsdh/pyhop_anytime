import unittest

import pyhop
from pyhop import TaskList


def go(state, entity, start, end):
    if state.loc[entity] == start and end in state.connected[start] and end not in state.visited[entity]:
        state.loc[entity] = end
        state.visited[entity].append(end)
        return state


def go_m(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    elif state.connected[start] == end:
        return TaskList([('go', entity, start, end)])
    else:
        return TaskList([[('go', entity, start, neighbor), ('go_method', entity, neighbor, end)] for neighbor in state.connected[start]])


def make_travel_planner():
    planner = pyhop.Planner()
    planner.declare_operators(go)
    planner.declare_methods('go_method', go_m)
    return planner


def setup_state(title, people, connections):
    state = pyhop.State(title)
    state.visited = {person: [] for (person,location) in people}
    state.loc = {person: location for (person,location) in people}
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
                            [('hero', 'mcrey312')],
                            [('mcrey312', 'hallway'), ('mcrey314', 'hallway'), ('lounge', 'hallway'), ('copyroom', 'lounge')])
        print(state)
        planner = make_travel_planner()
        plan = planner.pyhop(state, [('go_method', 'hero', 'mcrey312', 'copyroom')])
        self.assertEqual(plan, [('go', 'hero', 'mcrey312', 'hallway'), ('go', 'hero', 'hallway', 'lounge'), ('go', 'hero', 'lounge', 'copyroom')])


if __name__ == "__main__":
    unittest.main()