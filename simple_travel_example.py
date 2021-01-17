"""
The "travel from home to the park" example from my lectures.
Author: Dana Nau <nau@cs.umd.edu>, May 31, 2013
This file should work correctly in both Python 2.7 and Python 3.2.
"""
import unittest

import pyhop
from pyhop import MethodResult


def taxi_rate(dist):
    return 1.5 + 0.5 * dist


def walk(state, a, x, y):
    if state.loc[a] == x:
        state.loc[a] = y
        return state


def call_taxi(state, a, x):
    state.loc['taxi'] = x
    return state


def ride_taxi(state, a, x, y):
    if state.loc['taxi'] == x and state.loc[a] == x:
        state.loc['taxi'] = y
        state.loc[a] = y
        state.owe[a] = taxi_rate(state.dist[x][y])
        return state


def pay_driver(state, a):
    if state.cash[a] >= state.owe[a]:
        state.cash[a] = state.cash[a] - state.owe[a]
        state.owe[a] = 0
        return state


planner = pyhop.Planner()
planner.declare_operators(walk, call_taxi, ride_taxi, pay_driver)
print('')
planner.print_operators()


def travel_by_foot(state, a, x, y):
    if state.dist[x][y] <= 2:
        return MethodResult([('walk', a, x, y)])


def travel_by_taxi(state, a, x, y):
    if state.cash[a] >= taxi_rate(state.dist[x][y]):
        return MethodResult([('call_taxi', a, x), ('ride_taxi', a, x, y), ('pay_driver', a)])


planner.declare_methods('travel', travel_by_foot, travel_by_taxi)
print('')
planner.print_methods()

state1 = pyhop.State('state1')
state1.loc = {'me': 'home'}
state1.cash = {'me': 20}
state1.owe = {'me': 0}
state1.dist = {'home': {'park': 8}, 'park': {'home': 8}}

print("""
********************************************************************************
Call planner.pyhop(state1,[('travel','me','home','park')]) with different verbosity levels
********************************************************************************
""")

print("- If verbose=0 (the default), Pyhop returns the solution but prints nothing.\n")
planner.pyhop(state1, [('travel', 'me', 'home', 'park')])

print('- If verbose=1, Pyhop prints the problem and solution, and returns the solution:')
planner.pyhop(state1, [('travel', 'me', 'home', 'park')], 1)

print('- If verbose=2, Pyhop also prints a note at each recursive call:')
planner.pyhop(state1, [('travel', 'me', 'home', 'park')], 2)

print('- If verbose=3, Pyhop also prints the intermediate states:')
planner.pyhop(state1, [('travel', 'me', 'home', 'park')], 3)


class Test(unittest.TestCase):

    def test(self):
        plan = planner.pyhop(state1, [('travel', 'me', 'home', 'park')])
        self.assertEqual(plan, [('call_taxi', 'me', 'home'), ('ride_taxi', 'me', 'home', 'park'), ('pay_driver', 'me')])


if __name__ == '__main__':
    unittest.main()