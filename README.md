## Overview

This is an alternative implementation of the [pyhop](https://bitbucket.org/dananau/pyhop/src/master/)
planner created by [Dana Nau](http://www.cs.umd.edu/~nau/). Here are the main modifications:
* Each planner, defined by a set of operators and methods, is instantiated as 
  an object of the `Planner` class. This allows multiple distinct planners to 
  coexist in a single program.
* Operators and Methods return `None` when they are not applicable.
* Methods return a `TaskList` object to specify what should happen next. 
  `TaskList` objects represent the following scenarios:
  * Successful plan completion
  * Exactly one task list option.
  * Multiple task list options, one of which is to be selected nondeterministically
    by the planner.
* The introduction of nondeterministic task options enables the use of an
  [anytime](https://en.wikipedia.org/wiki/Anytime_algorithm) planning 
  algorithm. The user can specify a maximum time limit, and once that time
  expires it will return the best plan it found. 
  * The anytime planning implementation is inspired by the
    algorithm described for the [SHOP3](https://github.com/shop-planner/shop3) planner.
* States and goals are consolidated into a single data type. Printing states
  is simplified by the implementation of a `__repr__()` method.  
* Depth-first search is implemented using a Python list as a stack rather 
  than by recursion. This is intended for avoiding stack overflows when 
  finding long plans.

## HTN Planning

Pyhop is a hierarchical task network (HTN) planner. To use an HTN planner, one must specify the following:

* **State**: Complete description of the current world state. In Pyhop, you can use an arbitrary Python data structure to describe the state.
* **Operators**: Each operator describes a state transformation. Operators can optionally include preconditions. If a precondition is not met, the operator will fail. In Pyhop, you will write one Python function for each operator.
* **Methods**: Methods encode a planning algorithm that decomposes a task into operators and other methods. In Pyhop, you will write one Python function for each method.

## Example

The example below shows a state description of part of the 3rd floor of an office building. 
Several rooms are all connected to a hallway. The lounge is further connected to the copy room.
A robot is in room 312 and has not yet visited any other rooms.

```
# State
state = State('3rd-floor')
state.visited = {'robot': []}
state.loc = {'robot': 'mcrey312'}
state.connected = {'mcrey312': ['hallway', 'mcrey314'], 
                   'hallway': ['mcrey312', 'mcrey314', 'lounge'], 
				   'mcrey314': ['mcrey312', 'hallway'], 
				   'lounge': ['hallway', 'copyroom'], 
				   'copyroom': ['lounge']}
```

In this example, there is only one operator: `go`. The `go` operator moves an entity from one room to 
an adjacent room, and records the adjacent room as having been visited.

It makes sure the entity is in the starting room and has not already visited the ending room.
It also makes sure the rooms are connected.

```
def go(state, entity, start, end):
    if state.loc[entity] == start and end in state.connected[start] and end not in state.visited[entity]:
        state.loc[entity] = end
        state.visited[entity].append(end)
        return state
```

There is also only one method in this example. If the start and end are the same, it signals success.
If they are connected, it posts as a task the `go` operator. Otherwise, it posts a list of alternative
tasks: travel from `start` to a neighbor, then recursively post `find_route` to travel from that 
neighbor to the end.

```
def find_route(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    elif state.connected[start] == end:
        return TaskList([('go', entity, start, end)])
    else:
        return TaskList([[('go', entity, start, neighbor), ('find_route', entity, neighbor, end)] for neighbor in state.connected[start]])
```

## Anytime Planning

Pyhop employs a search strategy known as depth-first search to find a plan. When presented with multiple options, 
as in the third alternative above, it aggressively makes choices until it has a complete plan. Here is one plan
that the planner might produce in response to the task ``:
```
[('go', 'robot', 'mcrey312', 'mcrey314'), 
 ('go', 'robot', 'mcrey314', 'hallway'), 
 ('go', 'robot', 'hallway', 'lounge'), 
 ('go', 'robot', 'lounge', 'copyroom')]
```

With properly designed methods, this should produce a plan if one exists, but it is not guaranteed to be the 
shortest possible plan. If time permits, the planner can go back and try other alternatives, and see if they 
produce better plans. This is known as *anytime planning*. Here is an example of a shorter plan:

```
[('go', 'robot', 'mcrey312', 'hallway'), 
 ('go', 'robot', 'hallway', 'lounge'), 
 ('go', 'robot', 'lounge', 'copyroom')]])
```

In an anytime planner, a plan is ready to return as soon as the first depth-first search completes. An anytime 
planner will backtrack and try alternative plans as long as time is available. The multiple options in the third
method step above constitute a *nondeterministic choice*. These nondeterministic choices are the alternatives 
available to the anytime planner.

## License

Following the original 
[pyhop](https://bitbucket.org/dananau/pyhop/src/master/) implementation, 
this project is licensed under the 
[Apache License, Version 2.0 (the "License")](http://www.apache.org/licenses/LICENSE-2.0).

## Authorship

This project is a derivative work of the 
[pyhop](https://bitbucket.org/dananau/pyhop/src/master/)
planner created by [Dana Nau](http://www.cs.umd.edu/~nau/). 
All additions and modifications are authored by 
[Gabriel J. Ferrer](https://github.com/gjf2a).