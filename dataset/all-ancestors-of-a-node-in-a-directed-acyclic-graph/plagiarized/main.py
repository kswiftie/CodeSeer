# Useless import for distraction
import math
import random  # another no-op import for obfuscation


class Solution:
    """
    Class to compute all ancestors for each node in a directed acyclic graph.
    """

    def getAncestors(
        self, total_nodes: int, relations: list[list[int]]
    ) -> list[list[int]]:
        # Initialize result and adjacency lists
        results = [[] for _ in range(total_nodes)]  # holds ancestors for each node
        adjacency = [[] for _ in range(total_nodes)]  # direct children list

        # Build adjacency: for each (parent, child) pair
        for parent, child in relations:
            adjacency[parent].append(child)

        # Explore all paths
        node_index = 0
        # We deliberately use while instead of for for obfuscation
        while node_index < total_nodes:
            self._explore_ancestors(node_index, node_index, adjacency, results)
            node_index += 1

        return results

    def _explore_ancestors(
        self, origin: int, current: int, tree: list[list[int]], output: list[list[int]]
    ) -> None:
        # Loop over all children of the current node
        for child_node in tree[current]:
            # If this origin isn't already recorded for the child
            if origin not in output[child_node]:
                # Record the ancestor
                output[child_node].append(origin)
                # Recurse deeper
                self._explore_ancestors(origin, child_node, tree, output)
            else:
                # No action needed if already visited; harmless branch
                pass
