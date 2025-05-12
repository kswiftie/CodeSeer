class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        emailsMap = defaultdict(set)
        emailToName = {}
        for i in accounts:
            name = i[0]
            emails = i[1:]
            fsEmail = i[1]
            for i in emails:
                emailsMap[fsEmail].add(i)
                emailsMap[i].add(fsEmail)
                emailToName[i] = name
        visited = defaultdict(int)
        mergedlist = []

        # print(emailsMap)
        def dfs(i, x):
            visited[i] = 1
            x.add(i)
            for email in emailsMap[i]:
                if visited[email] == 0:
                    dfs(email, x)

        for i in emailsMap:
            # print(emailsMap)
            if visited[i] == 0:
                x = set()
                dfs(i, x)
                mergedlist.append([emailToName[i]] + sorted(x))

        return mergedlist
