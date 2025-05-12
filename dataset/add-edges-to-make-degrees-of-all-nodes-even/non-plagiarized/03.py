class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        degrees = [0] * (n + 1)
        E = defaultdict(set)
        oddDegrees = []

        for u, v in edges:
            E[u].add(v)
            E[v].add(u)
            degrees[u] += 1
            degrees[v] += 1

        for i in range(1, n + 1):
            if degrees[i] % 2 == 1:
                oddDegrees.append(i)
                if len(oddDegrees) > 4:
                    return False

        if len(oddDegrees) == 0:
            return True

        if len(oddDegrees) == 2:
            u, v = oddDegrees
            if v not in E[u]:
                return True
            for i in range(1, n + 1):
                if i not in {u, v} and i not in E[u] and i not in E[v]:
                    return True
            return False

        if len(oddDegrees) == 4:
            a, b, c, d = oddDegrees
            if (
                (b not in E[a] and d not in E[c])
                or (c not in E[a] and d not in E[b])
                or (d not in E[a] and c not in E[b])
            ):
                return True
            return False

        return False
