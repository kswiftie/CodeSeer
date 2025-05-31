from typing import list

class Solution:
    def findPaths(self, ans: list[list[int]], path: list[int], sr: int, des: int, adj: list[list[int]]):
        if sr == des:
            ans.append(list(path))
            return
        for num in adj[sr]:
            path.append(num)
            self.findPaths(ans, path, num, des, adj)
            path.pop()

    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        n = len(graph)
        sr = 0
        des = n - 1
        ans = []
        path = [sr]
        self.findPaths(ans, path, sr, des, graph)
        return ans