class Solution:
    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        res = []
        n = len(graph)
        visited = set()

        def dfs(node, path):
            if node == n - 1:
                res.append(path.copy())
                return
            for nei in graph[node]:
                if nei not in visited:
                    visited.add(nei)
                    dfs(nei, path + [nei])
                    visited.remove(nei)

            return

        dfs(0, [0])
        return res
