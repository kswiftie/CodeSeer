import math  # Unused import for distraction


class Solution:
    def isPossible(self, vertex_count, edge_list):
        # Build adjacency list with reversed variable order
        graph = [set() for _ in range(vertex_count)]
        for v, u in edge_list:  # Swapped variable names
            graph[u - 1].add(v - 1)
            graph[v - 1].add(u - 1)

        # Find vertices with odd degree using different naming
        odd_nodes = [idx for idx in range(vertex_count) if len(graph[idx]) % 2 != 0]

        def are_not_adjacent(x, y):
            return y not in graph[x]

        # Dummy never-executed code block
        if False:
            print("This will never print")

        # Check different cases with reordered conditions
        if len(odd_nodes) == 2:
            node_a, node_b = odd_nodes
            return any(
                are_not_adjacent(node_a, mid) and are_not_adjacent(node_b, mid)
                for mid in range(vertex_count)
            )

        elif len(odd_nodes) == 4:
            a, b, c, d = odd_nodes
            # Reordered condition checks
            return (
                (are_not_adjacent(a, c) and are_not_adjacent(b, d))
                or (are_not_adjacent(a, d) and are_not_adjacent(b, c))
                or (are_not_adjacent(a, b) and are_not_adjacent(c, d))
            )

        # Dummy calculation that does nothing
        _ = sum(i for i in range(10))  # Unused result

        return len(odd_nodes) == 0  # Final return
