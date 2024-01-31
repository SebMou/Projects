import pandas as pd

class Node:
    
    """
    This class creates a new node, with no children. 
    The all method also returns any children of the current node we are in
    (which will be defined below) if there are any, as well as the characters
    in the path leading to this node.
    """
        
    def __init__(self):
        self.EndOfWord = False
        self.children = {}

    def all(self, before):
        if self.EndOfWord:
            yield before

        for ch, child in self.children.items():
            yield from child.all(before + ch)

class Trie:
    
    """
    The method __init__ creates a new root node for our trie.
    The insert method starts at the root node. It then reads what we would like
    to input into the trie, and verifies if the path of characters already
    exists. If it does, nothing is done, if not, a new path is created by adding
    child nodes to the last character which is in our desired path.
    The complete method starts the root node. It checks wether any of the child
    nodes have the first character. If so, it moves on to that node, and checks
    if any of that node's child nodes have the second character, and so on.
    Once we reach the end of our input, assuming there was a possible path,
    the all method described above in the Node class provides us with our
    possible paths after the search input.
    """
    
    def __init__(self):
        self.root = Node()

    def insert(self, key):
        curr = self.root
        for ch in key:
            node = curr.children.get(ch)
            if not node:
                node = Node()
                curr.children[ch] = node
            curr = node
        curr.EndOfWord = True
    
    def complete(self, before):
        curr = self.root
        for c in before:
            curr = curr.children.get(c)
            if curr is None:
                return

        yield from curr.all(before)
        
        
"""
In this case, our testing data was comprised of two csv files with a list of
entries. These will be included in the repository and the directory in the
read_csv function below should be changed to match the directory of these files,
or another csv file you may want to read.
We then initialize a trie, insert each of our entries into it and print a list
of the results for "Amazon ", which should return ['Amazon Music', 'Amazon Shopping']
"""
possibs = pd.read_csv(r"C:\Users\Asus\Downloads\python-challenge-master\python-challenge-master\test_files\190titles.csv")

trie = Trie()

for row in possibs.itertuples():
    trie.insert(row.Name)
     
print(list(trie.complete('Amazon ')))
    
    
    
    
    
    
    
    
    
    

        
