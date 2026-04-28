class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.freq = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True
        node.freq += 1

    def search_prefix(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node


def dfs(node, prefix, results):
    if node.is_end:
        results.append((prefix, node.freq))

    for ch, child in node.children.items():
        dfs(child, prefix + ch, results)
