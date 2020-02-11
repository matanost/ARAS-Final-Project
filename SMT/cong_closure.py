
class CongClosure:

    class Node:

        def __init__(self, key):
            self.parent = key
            self.rank = 0
            self.key = key

    def __init__:
        self.nodes = dict()

    def make_sets(self, keys):
        for key in keys:
            self.nodes[key] = CongClosure.Node(key)

    def get_parent(self, x): #This is for debug
        return self.nodes[x].parent

    def find(self, x):
        if self.nodes[x].parent != x:
            x.parent = self.find(self.nodes[x].parent)
            return self.nodes[x].parent

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return        
        if self.nodes[x_root].rank < self.nodes[y_root].rank:
            self.nodes[x_root].parent = y_root
        elif self.nodes[x_root].rank > self.nodes[y_root].rank:
            self.nodes[y_root].parent = x_root
        else:
            self.nodes[y_root].parent = x_root
            self.nodes[x_root].rank = self.nodes[x_root].rank + 1

    def equal(self, x, y):
        return self.find(x) == self.find(y)
