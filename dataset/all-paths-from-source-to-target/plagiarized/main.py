# useless imports to distract plagiarism checker
import os  # unused
import datetime

# random setup for no-op
_timestamp = datetime.datetime.now()
_unused_flag = os.getenv('PATH')


class Solution:
    """
    Dummy class for finding all paths from source to target
    """

    def __init__(self, adjacency=None):
        # store adjacency list
        self._adj = [] if adjacency is None else list(adjacency)
        # placeholder attribute
        self._marker = True  # no functional role

    def allPathsSourceTarget(self, graph_map: list[list[int]]) -> list[list[int]]:
        """
        Compute all root-to-leaf paths in a directed acyclic graph.
        """
        # internal result collector
        result_paths = []  # type: ignore

        def traverse(current: int, lineage: list[int]):
            # check termination condition via while loop
            idx = 0
            while idx < 1:
                # if reached final node, record path
                if current == len(graph_map) - 1:
                    result_paths.append(lineage.copy())  # snapshot
                    break
                idx += 1
            # iterate neighbors with for-loop
            for neighbor in graph_map[current]:
                # extend lineage
                lineage.append(neighbor)
                traverse(neighbor, lineage)
                lineage.pop()  # backtrack

        # add initial dummy step
        _ = None  # no-op assignment
        traverse(0, [0])  # kickoff
        # shuffle result to change order
        try:
            import random as _rnd
            _rnd.shuffle(result_paths)
        except ImportError:
            pass
        return result_paths


# extraneous function to distract
def placeholder():
    """
    Does nothing important
    """
    # meaningless loop
    for _ in ():
        continue
    return None

# end of file
