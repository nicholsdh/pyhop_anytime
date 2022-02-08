import sys


def anyhop_main(planner):
    if len(sys.argv) == 1:
        print(f"Usage: python3 {sys.argv[0]} -v:[verbosity] -s:[max seconds] [planner_file]+")
    else:
        verbosity = 1
        max_seconds = None
        for filename in sys.argv[1:]:
            if filename.startswith("-v"):
                verbosity = int(filename.split(':')[1])
            elif filename.startswith("-s"):
                max_seconds = float(filename.split(':')[1])
            else:
                exec(open(filename).read())
                plans = planner.anyhop(state, [('start', goals)], max_seconds=max_seconds, verbose=verbosity)
                for (plan, time) in plans:
                    print(plan)
                for (plan, time) in plans:
                    print(f"Length: {len(plan)} time: {time}")
                print(len(plans), "total plans generated")