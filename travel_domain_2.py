import unittest

import pyhop
from pyhop import TaskList


def go(state, entity, start, end):
    if state.loc[entity] == start and end in state.connected[start] and end not in state.visited[entity]:
        state.loc[entity] = end
        state.visited[entity].append(end)
        return state


def find_route(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    elif state.connected[start] == end:
        return TaskList([('go', entity, start, end)])
    else:
        return TaskList([[('go', entity, start, neighbor), ('find_route', entity, neighbor, end)] for neighbor in state.connected[start]])


def make_travel_planner():
    planner = pyhop.Planner()
    planner.declare_operators(go)
    planner.declare_methods('find_route', find_route)
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
                            [('mcrey312', 'hallway'), ('mcrey312', 'mcrey314'), ('mcrey314', 'hallway'), ('lounge', 'hallway'), ('copyroom', 'lounge')])
        print(state)
        planner = make_travel_planner()
        plans = planner.anyhop(state, [('find_route', 'hero', 'mcrey312', 'copyroom')])
        print(plans)
        plans = [plan for (plan, time) in plans]
        self.assertEqual(plans, [[('go', 'hero', 'mcrey312', 'mcrey314'), ('go', 'hero', 'mcrey314', 'hallway'), ('go', 'hero', 'hallway', 'lounge'), ('go', 'hero', 'lounge', 'copyroom')], [('go', 'hero', 'mcrey312', 'hallway'), ('go', 'hero', 'hallway', 'lounge'), ('go', 'hero', 'lounge', 'copyroom')]])
        plan = planner.pyhop(state, [('find_route', 'hero', 'mcrey312', 'no-room')])
        self.assertEqual(plan, None)


if __name__ == "__main__":
    unittest.main()