import numpy as np
import pandas as pd
import json

class TrieNode(object):

    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.word_finished = False


def add(root, word: str):
    word = word.lower().replace('ё', 'е')  #lower- преобразует все символы в нижний регистр, replace меняет ё на е
    node = root
    for char in word:
        found_in_child = False
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                break
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            node = new_node
    node.word_finished = True

def prefix_descent(root, prefix: str):
    node = root
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
        if char_not_found:
            return False
    return node


def trie_print(node, string, level, list_of_strings):
    if node.word_finished:
        res_string = ''.join(string)
        list_of_strings.append(res_string)
    else:
        for child in node.children:
            string.insert(level, child.char)
            trie_print(child, string.copy(), level+1, list_of_strings)
            string.pop()


def suggester(root, prefix):
    prefix = prefix.lower()
    node = prefix_descent(root, prefix)
    list_of_strings = []
    string = []
    if type(node) == bool:
        list_of_strings.append(prefix)
    else:
        trie_print(node, string, 0, list_of_strings)
        for i in range(len(list_of_strings)):
            list_of_strings[i] = prefix + list_of_strings[i]
    return list_of_strings


def rating(root, word , number: int,data:pd.DataFrame):
    string = suggester(root, word)
    sugg_data = pd.DataFrame(columns =  ["name", "rating"])
    n = len(data)
    i = 0
    while i < n:
        for s in string:
            if data.at[i, 'name'] == s:
                sugg_data = pd.DataFrame(np.array([[data.loc[i]['name'], data.loc[i]['rating']]]), columns=['name', 'rating']).append(sugg_data, ignore_index=True)
        i += 1
    sugg_data['rating'] = sugg_data['rating'].apply(lambda x: int(x))
    sugg_data = sugg_data.sort_values(['rating'], ascending=[0])
    sugg_data = sugg_data[:number]
    #string = sugg_data['name']
    return list(sugg_data['name'])
