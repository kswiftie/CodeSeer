class Solution:
    def judgePoint24(self, cards: list[int]) -> bool:
        if len(cards) == 2:
            return abs((cards[0] + cards[1]) - 24) < 0.00001 or \
                abs((cards[0] * cards[1]) - 24) < 0.00001 or \
                abs((cards[0] - cards[1]) - 24) < 0.00001 or \
                abs((cards[1] - cards[0]) - 24) < 0.00001 or \
                abs((cards[1] and (cards[0] / cards[1])) - 24) < 0.00001 or \
                abs((cards[0] and (cards[1] / cards[0])) - 24) < 0.00001

        for i in range(len(cards) - 1):
            cards[0], cards[i] = cards[i], cards[0]
            for j in range(i + 1, len(cards)):
                cards[1], cards[j] = cards[j], cards[1]
                computations = [
                    cards[0] + cards[1],
                    cards[0] * cards[1],
                    cards[0] - cards[1],
                    cards[1] - cards[0],
                    cards[1] and cards[0] / cards[1],
                    cards[0] and cards[1] / cards[0]
                ]
                remaining = cards[2:]
                for computation in computations:
                    found = self.judgePoint24(remaining + [computation])
                    if found:
                        return True
                cards[1], cards[j] = cards[j], cards[1]
            cards[0], cards[i] = cards[i], cards[0]
        return False
