import numpy as np

def from_dictionnary(dictionnary):
    """
    Create Suffix Tree from a list of words
    :param dictionnary: list of words
    :return: Suffix Tree
    """
    tree = SuffixTree()
    for word in dictionnary:
        tree.add(word)
    return tree

def from_file(filename):
    """
    Load Suffix Tree from a file
    :param filename:
    :return: Suffix Tree
    """
    tree = SuffixTree()
    with open(filename, 'r') as fd:
        previous_indentation = 0
        current_node = tree.root
        for line in fd:
            line = line[:-1]

            indentation = 0
            for w in line:
                if w != ' ':
                    break
                indentation += 1

            value, is_word = line[indentation:].split(' ')
            is_word = True if is_word == '1' else False

            if indentation > previous_indentation:
                current_node = current_node.children[-1]
                previous_indentation = indentation
            elif indentation < previous_indentation:
                while indentation < previous_indentation:
                    current_node = current_node.parent
                    previous_indentation -= 1
            current_node.children.append(Node(current_node, value, is_word=is_word))
    return tree

def to_list(tree):
    """
    Convert a Suffix Tree to a list
    :param tree: suffix tree
    :return:
    """
    l = []
    _to_list(tree.root, '', l)
    return l

def _to_list(node, suffix, list):
    """
    Recursive conversion of a suffix tree to a list
    You should use 'to_list(tree)'
    :param node:
    :param suffix:
    :param list:
    """
    suffix = suffix + node.value
    if node.is_word:
        list.append(suffix)
    for child in node.children:
        _to_list(child, suffix, list)

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
        s = ''
        for child in self.root.children:
            s += str(child) + '\n'
        return s

    def __len__(self):
        return len(self.root)

    def save(self, filename):
        with open(filename, 'w') as fd:
            for child in self.root.children:
                child.write(fd)

class Node:

    def __init__(self, parent, value, is_word=False):
        self.parent = parent
        self.value = value
        self.children = []
        self.is_word = is_word

    def __contains__(self, value):
        if not value.startswith(self.value) and len(self.value) > 0:
            return False

        if value == self.value:
            return self.is_word

        val = value[len(self.value):]
        if len(val) < 1:
            return False
        for child in self.children:
            if val in child: return True
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

    def write(self, file, indentation=''):
        file.write('{}{} {}\n'.format(indentation, self.value, '1' if self.is_word else '0'))
        for child in self.children:
            child.write(file, indentation+' ')