"""
Blocks World domain definition for Pyhop 1.1.
Author: Dana Nau <nau@cs.umd.edu>, November 15, 2012
This file should work correctly in both Python 2.7 and Python 3.2.
"""

import pyhop
from pyhop import TaskList

"""Each Pyhop planning operator is a Python function. The 1st argument is
the current state, and the others are the planning operator's usual arguments.
This is analogous to how methods are defined for Python classes (where
the first argument is always the name of the class instance). For example,
the function pickup(state,b) implements the planning operator for the task
('pickup', b).

The blocks-world operators use three state variables:
- pos[b] = block b's position, which may be 'table', 'hand', or another block.
- clear[b] = False if a block is on b or the hand is holding b, else True.
- holding = name of the block being held, or False if the hand is empty.
"""


def pickup(state, b):
    if state.pos[b] == 'table' and state.clear[b] == True and state.holding == False:
        state.pos[b] = 'hand'
        state.clear[b] = False
        state.holding = b
        return state


def putdown(state, b):
    if state.pos[b] == 'hand':
        state.pos[b] = 'table'
        state.clear[b] = True
        state.holding = False
        return state


def unstack(state, b, c):
    if state.pos[b] == c and c != 'table' and state.clear[b] == True and state.holding == False:
        state.pos[b] = 'hand'
        state.clear[b] = False
        state.holding = b
        state.clear[c] = True
        return state


def stack(state, b, c):
    if state.pos[b] == 'hand' and state.clear[c] == True:
        state.pos[b] = c
        state.clear[b] = True
        state.holding = False
        state.clear[c] = False
        return state


"""
Here are some helper functions that are used in the methods' preconditions.
"""


def is_done(b1,state,goal):
    if b1 == 'table': return True
    if b1 in goal.pos and goal.pos[b1] != state.pos[b1]:
        return False
    if state.pos[b1] == 'table': return True
    return is_done(state.pos[b1],state,goal)


def status(b1,state,goal):
    if is_done(b1,state,goal):
        return 'done'
    elif not state.clear[b1]:
        return 'inaccessible'
    elif not (b1 in goal.pos) or goal.pos[b1] == 'table':
        return 'move-to-table'
    elif is_done(goal.pos[b1],state,goal) and state.clear[goal.pos[b1]]:
        return 'move-to-block'
    else:
        return 'waiting'


def all_blocks(state):
    return state.clear.keys()


"""
In each Pyhop planning method, the first argument is the current state (this is analogous to Python methods, in which the first argument is the class instance). The rest of the arguments must match the arguments of the task that the method is for. For example, ('pickup', b1) has a method get_m(state,b1), as shown below.
"""

### methods for "move_blocks"


def move_blocks(state, goal):
    """
    This method implements the following block-stacking algorithm:
    If there's a block that can be moved to its final position, then
    do so and call move_blocks recursively. Otherwise, if there's a
    block that needs to be moved and can be moved to the table, then
    do so and call move_blocks recursively. Otherwise, no blocks need
    to be moved.
    """

    if all((status(b, state, goal) == 'done' for b in all_blocks(state))):
        return TaskList(completed=True)

    for b1 in all_blocks(state):
        s = status(b1,state,goal)
        if s == 'move-to-table':
            return TaskList([('move_one', b1, 'table'), ('move_blocks', goal)])
        elif s == 'move-to-block':
            return TaskList([('move_one', b1, goal.pos[b1]), ('move_blocks', goal)])

    #
    # if we get here, no blocks can be moved to their final locations
    # This solution deviates from the original Pyhop solution by incorporating
    # nondeterminism.
    return TaskList([[('move_one', b, 'table'), ('move_blocks', goal)]
                     for b in all_blocks(state) if status(b, state, goal) == 'waiting'])


### methods for "move_one"

def move_one(state, b1, dest):
    """
    Generate subtasks to get b1 and put it at dest.
    """
    if state.pos[b1] != dest:
        return TaskList([('get', b1), ('put', b1, dest)])


### methods for "get"

def get(state, b1):
    """
    Generate either a pickup or an unstack subtask for b1.
    """
    if state.clear[b1]:
        if state.pos[b1] == 'table':
            return TaskList([('pickup', b1)])
        else:
            return TaskList([('unstack', b1, state.pos[b1])])


### methods for "put"

def put(state, b1, b2):
    """
    Generate either a putdown or a stack subtask for b1.
    b2 is b1's destination: either the table or another block.
    """
    if state.holding == b1:
        if b2 == 'table':
            return TaskList([('putdown', b1)])
        else:
            return TaskList([('stack', b1, b2)])


def make_blocks_planner():
    blocks_planner = pyhop.Planner()

    """
    Below, 'declare_operators(pickup, unstack, putdown, stack)' tells Pyhop
    what the operators are. Note that the operator names are *not* quoted.
    """
    blocks_planner.declare_operators(pickup, unstack, putdown, stack)

    """
    declare_methods must be called once for each taskname. Below, 'declare_methods('get',get_m)' tells Pyhop that 'get' has one method, get_m. Notice that 'get' is a quoted string, and get_m is the actual function.
    """

    blocks_planner.declare_methods('move_blocks', move_blocks)
    blocks_planner.declare_methods('move_one', move_one)
    blocks_planner.declare_methods('get', get)
    blocks_planner.declare_methods('put', put)
    return blocks_planner
