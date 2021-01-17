import copy
import sys
import time


class State:
    def __init__(self, name):
        self.__name__ = name

    def __repr__(self):
        return '\n'.join([f"{self.__name__}.{name} = {val}" for (name, val) in vars(self).items() if name != "__name__"])


class Planner:
    def __init__(self, verbose=0):
        self.operators = {}
        self.methods = {}
        self.verbose = verbose

    def declare_operators(self, *op_list):
        self.operators.update({op.__name__:op for op in op_list})

    def declare_methods(self, task_name, *method_list):
        self.methods.update({task_name: list(method_list)})

    def print_operators(self):
        print(f'OPERATORS: {", ".join(self.operators)}')

    def print_methods(self):
        print('{:<14}{}'.format('TASK:','METHODS:'))
        for task in self.methods:
            print('{:<14}'.format(task) + ', '.join([f.__name__ for f in self.methods[task]]))

    def log(self, min_verbose, msg):
        if self.verbose >= min_verbose:
            print(msg)

    def log_state(self, min_verbose, msg, state):
        if self.verbose >= min_verbose:
            print(msg)
            print_state(state)

    def pyhop(self, state, tasks, verbose=0):
        self.verbose = verbose
        self.log(1, f"** pyhop, verbose={self.verbose}: **\n   state = {state.__name__}\n   tasks = {tasks}")
        options = [PlanStep([], tasks, state)]
        while len(options) > 0:
            candidate = options.pop()
            if self.verbose >= 4:
                input("Enter a key:")
            self.log(2, f"depth {candidate.depth()} tasks {candidate.tasks}")
            self.log(3, f"plan: {candidate.plan}")
            if candidate.complete():
                self.log(3, f"depth {candidate.depth()} returns plan {candidate.plan}")
                self.log(1, f"** result = {candidate.plan}\n")
                return candidate.plan
            else:
                options.extend(candidate.successors(self))

    def anyhop(self, state, tasks, max_seconds=None, verbose=0):
        start_time = time.time()
        self.verbose = verbose
        self.log(1, f"** anyhop, verbose={self.verbose}: **\n   state = {state.__name__}\n   tasks = {tasks}")
        options = [PlanStep([], tasks, state)]
        plans = []
        while len(options) > 0 and (max_seconds is None or time.time() - start_time < max_seconds):
            candidate = options.pop()
            if len(plans) == 0 or len(candidate.plan) < len(plans[-1]):
                self.log(2, f"depth {candidate.depth()} tasks {candidate.tasks}")
                self.log(3, f"plan: {candidate.plan}")
                if candidate.complete():
                    self.log(3, f"depth {candidate.depth()} returns plan {candidate.plan}")
                    self.log(1, f"** result = {candidate.plan}\n")
                    plans.append((candidate.plan, time.time() - start_time))
                else:
                    options.extend(candidate.successors(self))
        return plans

    def anyhop_best(self, state, tasks, max_seconds=None, verbose=0):
        plans = self.anyhop(state, tasks, max_seconds, verbose)
        return plans[-1][0]

    def anyhop_stats(self, state, tasks, max_seconds=None, verbose=0):
        plans = self.anyhop(state, tasks, max_seconds, verbose)
        return [(len(plan), time) for (plan, time) in plans]

def print_state(state, indent=4):
    if state is not None:
        for (name,val) in vars(state).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(state.__name__ + '.' + name)
                print(' =', val)
    else:
        print('False')


class PlanStep:
    def __init__(self, plan, tasks, state):
        self.plan = plan
        self.tasks = tasks
        self.state = state

    def depth(self):
        return len(self.plan)

    def complete(self):
        return len(self.tasks) == 0

    def successors(self, planner):
        options = []
        self.add_operator_options(options, planner)
        self.add_method_options(options, planner)
        if len(options) == 0:
            planner.log(3, f"depth {self.depth()} returns failure")
        return options

    def add_operator_options(self, options, planner):
        next_task = self.tasks[0]
        if next_task[0] in planner.operators:
            planner.log(3, f"depth {self.depth()} action {next_task}")
            operator = planner.operators[next_task[0]]
            newstate = operator(copy.deepcopy(self.state), *next_task[1:])
            planner.log_state(3, f"depth {self.depth()} new state:", newstate)
            if newstate:
                options.append(PlanStep(self.plan + [next_task], self.tasks[1:], newstate))

    def add_method_options(self, options, planner):
        next_task = self.tasks[0]
        if next_task[0] in planner.methods:
            planner.log(3, f"depth {self.depth()} method instance {next_task}")
            relevant = planner.methods[next_task[0]]
            for method in relevant:
                subtask_options = method(self.state, *next_task[1:])
                if subtask_options is not None:
                    for subtasks in subtask_options:
                        planner.log(3, f"depth {self.depth()} new tasks: {subtasks}")
                        options.append(PlanStep(self.plan, subtasks + self.tasks[1:], self.state))


############################################################
# Helper functions that may be useful in domain models


def forall(seq,cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True


def find_if(cond,seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x):
            return x