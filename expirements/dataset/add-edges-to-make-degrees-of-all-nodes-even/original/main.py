class Solution:
    def isPossible(self, n, edges):
        G = [set() for i in range(n)]
        for i, j in edges:
            G[i - 1].add(j - 1)
            G[j - 1].add(i - 1)
        odd = [i for i in range(n) if len(G[i]) % 2]

        def f(a, b):
            return a not in G[b]

        if len(odd) == 2:
            a, b = odd
            return any(f(a, i) and f(b, i) for i in range(n))

        if len(odd) == 4:
            a, b, c, d = odd
            return f(a, b) and f(c, d) or \
                f(a, c) and f(b, d) or \
                f(a, d) and f(c, b)
        return len(odd) == 0
