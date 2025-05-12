class Solution:
    def alertNames(self, keyName: list[str], keyTime: list[str]) -> list[str]:

        d, alerts = defaultdict(list), []
        keyTime = map(lambda x: int(x[:2]) * 60 + int(x[3:]), keyTime)  # <-- 1.

        for name, time in zip(keyName, keyTime):  # <-- 2.
            d[name].append(time)

        for name in d:  # <-- 3.
            uses = sorted(d[name])
            if any(third - first <= 60 for third, first in zip(uses[2:], uses)):
                alerts.append(name)  # <-- 4.

        return sorted(alerts)
