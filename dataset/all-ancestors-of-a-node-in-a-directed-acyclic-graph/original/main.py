class Solution:
    def getAncestors(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        ans = [[] for _ in range(n)]
        directChild = [[] for _ in range(n)]
        for e in edges:
            directChild[e[0]].append(e[1])
        for i in range(n):
            self.dfs(i, i, ans, directChild)
        return ans

    def dfs(
        self, x: int, curr: int, ans: list[list[int]], directChild: list[list[int]]
    ) -> None:
        for ch in directChild[curr]:
            if not ans[ch] or ans[ch][-1] != x:
                ans[ch].append(x)
                self.dfs(x, ch, ans, directChild)
