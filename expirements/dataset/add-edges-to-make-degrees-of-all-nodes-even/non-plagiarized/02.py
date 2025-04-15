class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        graph = [set() for _ in range(n)]
        for u, v in edges:
            graph[u - 1].add(v - 1)
            graph[v - 1].add(u - 1)
        odd = [i for i, x in enumerate(graph) if len(x) & 1]
        return len(odd) == 0 or len(odd) == 2 and any(
            odd[0] not in graph[x] and odd[1] not in graph[x] for x in range(n)) or len(odd) == 4 and (
                odd[0] not in graph[odd[1]] and odd[2] not in graph[odd[3]] or odd[0] not in graph[odd[2]] and odd[
            1] not in graph[odd[3]] or odd[0] not in graph[odd[3]] and odd[1] not in graph[odd[2]])
