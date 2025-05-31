class Solution:
    def getAncestors(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        def dfs(ancestor: int, kid: int) -> None:
            if not (ans[kid] and ans[kid][-1] == ancestor):
                if kid != ancestor:
                    ans[kid].append(ancestor)
                for grand_child in parent_to_kids[kid]:
                    dfs(ancestor, grand_child)

        parent_to_kids = defaultdict(list)
        for parent, kid in edges:
            parent_to_kids[parent].append(kid)
        ans = [[] for _ in range(n)]
        for i in range(n):
            dfs(i, i)
        return ans
