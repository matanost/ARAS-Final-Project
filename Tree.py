# class Operator(Enum):
#     AND = '&'
#     OR = '||'
#     NOT = "-"
#     IF = "->"
#     IFF = "<->"


class Node:

    def __init__(self, parent, value):
        self.left_son = None
        self.right_son = None
        self.parent = parent
        self.value = value

    # def set_parent(self, parent_node):
    #     self.parent = parent_node

    def set_left_son(self, val):
        self.left_son = Node(self, val)

    def set_right_son(self, val):
        self.right_son = Node(self, val)

    def set_value(self, value):
        self.value = value

    def remove_parent(self):
        self.parent = None        

    def remove_left_son(self):
        self.left_son = None

    def remove_right_son(self):
        self.right_son = None        

    def has_left_son(self):
        if self.left_son is None:
            return False
        return True

    def has_right_son(self):
        if self.right_son is None:
            return False
        return True

    def is_leaf(self):
        return not (self.has_right_son() and self.has_left_son())

    def get_parent(self):
        return self.parent

    def get_right_son(self):
        if self.has_right_son():
            return self.right_son
        return self.has_right_son()

    def get_left_son(self):
        if self.has_left_son():
            return self.left_son
        return self.has_left_son()

    def get_value(self):
        return self.value

    def __str__(self):
        str_n = lambda n : "None" if (n is None) else str(n.value)
        out = "<val=" + str_n(self) + ", parent=" + str_n(self.parent) + ", left=" + str_n(self.left_son) + ", right=" + str_n(self.right_son) +">\n"
        out += str(self.left_son)
        out += str(self.right_son)

class Tree:

    def __init__(self, val):
        self.root = Node(None, val)
        #self.nodes = [root]

    def get_root(self):
        return self.root

    # def create_left_son(self, parent, son_value):
    #     son = Node(parent)
    #     son.set_value(son_value)
    #     parent.set_left_son(son)
    #     self.nodes.append(son)

    # def create_right_son(self, parent, son_value):
    #     son = Node(parent)
    #     son.set_value(son_value)
    #     parent.set_right_son(son)
    #     self.nodes.append(son)
