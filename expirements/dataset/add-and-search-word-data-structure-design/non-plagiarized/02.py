class WordDictionary:

    def __init__(self):
        self.trie = dict()

    def addWord(self, word: str) -> None:
        node = self.trie
        for ch in word + "🌻":
            if ch not in node:
                node[ch] = dict()

            node = node[ch]

    def search(self, word: str) -> bool:
        nodes = [self.trie]
        for ch in word + "🌻":
            newNodes = []
            for node in nodes:
                if ch == ".":
                    newNodes += [v for v in node.values()]
                elif ch in node:
                    newNodes.append(node[ch])

            if not newNodes:
                return False

            nodes = newNodes

        return True
