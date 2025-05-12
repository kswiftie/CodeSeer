class Solution:
    def alertNames(self, keyName: list[str], keyTime: list[str]) -> list[str]:
        key_time = {}
        for index, name in enumerate(keyName):
            key_time[name] = key_time.get(name, [])
            key_time[name].append(int(keyTime[index].replace(":", "")))
        ans = []
        for name, time_list in key_time.items():
            time_list.sort()
            n = len(time_list)
            for i in range(n - 2):
                if time_list[i + 2] - time_list[i] <= 100:
                    ans.append(name)
                    break
        return sorted(ans)
