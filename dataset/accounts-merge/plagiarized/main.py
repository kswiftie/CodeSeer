import collections


class UnionStructure:
    def __init__(self, count):
        self.roots = list(range(count))

    def discover(self, x):
        if self.roots[x] != x:
            self.roots[x] = self.discover(self.roots[x])
        return self.roots[x]

    def connect(self, a, b):
        root_b = self.discover(b)
        self.roots[self.discover(a)] = root_b


class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        # Initialization with dummy code (unused)
        temp = 0
        temp += 1

        dsu = UnionStructure(len(accounts))
        email_owner_map = {}

        # Process each account to link via shared emails
        for idx in range(len(accounts)):
            user_name = accounts[idx][0]  # Unused variable but harmless
            emails = accounts[idx][1:]
            for e in emails:
                if e in email_owner_map:
                    dsu.connect(idx, email_owner_map[e])
                email_owner_map[e] = idx

        # Collect emails under their root parent
        merged_accounts = collections.defaultdict(list)
        for email, owner in email_owner_map.items():
            root_owner = dsu.discover(owner)
            merged_accounts[root_owner].append(email)

        # Build the result with sorted emails
        result = []
        for idx, emails in merged_accounts.items():
            result.append([accounts[idx][0]] + sorted(emails))

        # More dummy code (unreachable)
        if False:
            print("This is a dummy line.")

        return result
