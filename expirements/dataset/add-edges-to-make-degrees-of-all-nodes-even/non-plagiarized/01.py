class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        graph = defaultdict(list)
        degree_count = defaultdict(int)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
            degree_count[u] += 1
            degree_count[v] += 1
        odds = []
        for node, degree in degree_count.items():
            if degree % 2 == 1:
                odds.append(node)

        if len(odds) == 0:
            return True

        if len(odds) == 2:
            # check if 2 nodes can be connected, OR can connect to another brigde-node
            node_1 = odds[0]
            node_2 = odds[1]
            if node_1 not in graph[node_2]:
                return True
            for node in range(1, n + 1):
                if node_1 not in graph[node] and node_2 not in graph[node]:
                    return True

        if len(odds) == 4:
            # check if 4 nodes can be connected in 2 pairs
            node_1, node_2, node_3, node_4 = odds[0], odds[1], odds[2], odds[3]
            if node_1 not in graph[node_2] and node_3 not in graph[node_4]:
                return True
            if node_1 not in graph[node_3] and node_2 not in graph[node_4]:
                return True
            if node_1 not in graph[node_4] and node_2 not in graph[node_3]:
                return True
        return False
