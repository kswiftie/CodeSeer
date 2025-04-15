class Solution:
    def isAdditiveNumber(self, num: str) -> bool:
        res = []

        def dfs(s, path):
            if not s: return len(path) >= 3
            for i in range(1,
                           len(s) + 1):  # Loop from 1 to len(s)+1, because we want our input(s[:i]) to have between 1 character to all the characters.
                if self.is_valid(s[:i], path):
                    if dfs(s[i:], path + [int(s[:i])]):
                        return True
            return False

        return dfs(num, [])

    def is_valid(self, s, path):
        if len(s) > 1 and s[0] == '0':  # Make sure input doesn't contain leading zero
            return False
        return len(path) < 2 or (path[-1] + path[-2] == int(s))
