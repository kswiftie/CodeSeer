class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        email_to_name = {}
        graph = {}
        for account in accounts:
            name = account[0]
            for email in account[1:]:
                email_to_name[email] = name
                if email not in graph:
                    graph[email] = set()
                if len(account) > 2:
                    first_email = account[1]
                    graph[first_email].add(email)
                    graph[email].add(first_email)

        def dfs(email, visited, component):
            visited.add(email)
            component.append(email)
            for neighbor in graph[email]:
                if neighbor not in visited:
                    dfs(neighbor, visited, component)

        visited = set()
        result = []
        for email in graph:
            if email not in visited:
                component = []
                dfs(email, visited, component)
                result.append([email_to_name[email]] + sorted(component))
        return result
