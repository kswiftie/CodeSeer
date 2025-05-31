class Solution:
    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        def backtrack(path, idx):
            if idx == n - 1:
                res.append(list(path))
                return

            for i in graph[idx]:
                path.append(i)
                backtrack(path, i)
                path.pop()

        n = len(graph)
        res = []
        backtrack([0], 0)
        return res
