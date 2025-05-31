class Solution:
    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        res = []

        def dfs(node, path):
            if node == len(graph) - 1:
                res.append(list(path))
                return
            for nei in graph[node]:
                path.append(nei)
                dfs(nei, path)
                path.pop()

        dfs(0, [0])
        return res