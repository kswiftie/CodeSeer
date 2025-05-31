class AllOne:
    def __init__(self):
        self.count = defaultdict(int)
        self.freq = defaultdict(set)

    def inc(self, key: str) -> None:
        cnt = self.count[key]
        if cnt > 0:
            self.freq[cnt].remove(key)
        self.count[key] += 1
        self.freq[cnt + 1].add(key)
        if not self.freq[cnt]:
            del self.freq[cnt]

    def dec(self, key: str) -> None:
        cnt = self.count[key]
        self.freq[cnt].remove(key)
        if cnt == 1:
            del self.count[key]
        else:
            self.count[key] -= 1
            self.freq[cnt - 1].add(key)
        if not self.freq[cnt]:
            del self.freq[cnt]

    def getMaxKey(self) -> str:
        return next(iter(self.freq[max(self.freq)]), "") if self.freq else ""

    def getMinKey(self) -> str:
        return next(iter(self.freq[min(self.freq)]), "") if self.freq else ""
