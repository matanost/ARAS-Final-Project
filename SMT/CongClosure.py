
class CongClosure:

    class Node:

        def __init__(self, key):
            self.parent = key
            self.rank = 0
            self.key = key

        def __str__(self):
            return "(k=" + str(self.key) + ",r=" + str(self.rank) + ")=>p=" + str(self.parent) + "\t"

    def __init__(self):
        self.nodes = dict()

    def make_sets(self, keys):
        for key in keys:
            self.nodes[key] = CongClosure.Node(key)

    def find(self, x):
        if self.nodes[x].parent != x:
            self.nodes[x].parent = self.find(self.nodes[x].parent)
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

    def __str__(self):
        out =  ("------------------------------\n")
        out += ("Congruance Closure=\n")
        for i,n in enumerate(self.nodes.values()):
            out += str(n)
            WIDTH = 10
            if (i % WIDTH) == WIDTH-1:
                out += "\n"
        out += ("------------------------------\n")
        return out
