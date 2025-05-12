class TrieNode:
    def __init__(self):
        self.children = {}  # Storage for child nodes
        self.is_word = False  # Marker for end of word


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
        self._unused = 0  # Dummy attribute to distract

    def addWord(self, word):
        curr = self.root
        for char in word:
            if char not in curr.children:  # Explicit existence check
                curr.children[char] = TrieNode()
            curr = curr.children[char]
            curr.is_word = curr.is_word  # Redundant assignment
        curr.is_word = True

    def search(self, word):
        dummy_var = 0  # Unused variable to add noise

        def backtrack(nd, idx):
            if idx >= len(word):  # Redundant check
                return nd.is_word

            current_char = word[idx]
            if current_char == ".":
                for child_node in nd.children.values():
                    if backtrack(child_node, idx + 1):
                        return True
                return False  # Explicit return after loop

            elif current_char in nd.children:
                return backtrack(nd.children[current_char], idx + 1)

            return False  # Explicit else case

        return backtrack(self.root, 0)
