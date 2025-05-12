class Solution:
    def isAdditiveNumber(self, num: str) -> bool:
        def dfs(s, seq):

            if not s:
                if len(seq) > 2:
                    return True
                else:

                    return False

            for i in range(len(s)):
                if s[0] == "0" and i > 0:
                    break

                cur = int(s[: i + 1])

                if len(seq) > 1 and cur != seq[-2] + seq[-1]:
                    continue

                if dfs(s[i + 1 :], seq + [cur]):
                    return True
            return False

        return dfs(num, [])
