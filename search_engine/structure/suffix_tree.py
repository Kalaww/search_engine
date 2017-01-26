import numpy as np

def from_sorted_dictionnary(dictionnary):
    """
    Create Suffix Tree from a list of words
    :param dictionnary: list of words
    :return: Suffix Tree
    """
    tree = SuffixTree()
    for word in dictionnary:
        tree.add(word)
    return tree

def get_suffix(word1, word2):
    """
    Suffix between two words
    :param word1:
    :param word2:
    :return:
    """
    l = len(word1) if len(word1) < len(word2) else len(word2)
    s = ''
    for i in range(l):
        if word1[i] == word2[i]:
            s += word1[i]
        else:
            break
    return s

class SuffixTree:

    def __init__(self):
        self.root = Node(None, '')

    def __contains__(self, value):
        return value in self.root

    def add(self, value):
        self.root.add(value)

    def __str__(self):
        return ''.join(str(self.root))

    def __len__(self):
        return len(self.root)

class Node:

    def __init__(self, parent, value, is_word=False):
        self.parent = parent
        self.value = value
        self.children = []
        self.is_word = is_word

    def __contains__(self, value):
        if self.value.startswith(value):
            if len(value) == len(self.value):
                return self.is_word
            val = value[len(self.value):]
            if self.children:
                for child in self.children:
                    return val in child
            else:
                return False

    def add(self, _value):
        if self.value == _value:
            self.is_word = True
            return
        value = _value[len(self.value):]
        for child in self.children:
            if value.startswith(child.value):
                child.add(value)
                return
            suffix = get_suffix(value, child.value)
            if len(suffix) > 0:
                node = Node(child, child.value[len(suffix):], is_word=child.is_word)
                node.children = child.children
                child.value = suffix
                child.is_word = suffix == value
                child.children = [node]
                if len(value[len(suffix):]) > 0:
                    child.children.append(Node(child, value[len(suffix):], is_word=True))
                return
        self.children.append(Node(self, value, is_word=True))

    def __str__(self):
        children = []
        for child in self.children:
            s = str(child)
            children.append(''.join(['\n\t'+l for l in s.split('\n')]))
        s = '{} {}'.format(self.value, '#' if self.is_word else '')
        return s + ''.join(children)

    def __len__(self):
        l = (1 if self.is_word else 0)
        if len(self.children) > 0:
            l += np.sum([len(child) for child in self.children])
        return l