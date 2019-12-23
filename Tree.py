class Operator(Enum):
    AND
    OR
    NOT

class Node:

    def __init__(self):
        self.left_son = None
        self.right_son = None
        self.parent = None

    def set_parent(self, parent_node):
        self.parent = parent_node

    def set_left_son(self, son_node):
        self.left_son = son_node

    def set_right_son(self, son_node):
        self.right_son = son_node

    def set_value(self,value):
        self.value = value

    def remove_parent(self):
        self.parent = None        

    def remove_left_son(self):
        self.left_son = None

    def remove_right_son(self):
        self.right_son = None        

    def has_left_son(self):
        return self.left_son is None

    def has_right_son(self):
        return self.right_son is None            

    def is_leaf(self):
        return not (self.has_right_son() and self.has_left_son())

    
class Tree:

    def __init__(self):
        root = Node()
        self.nodes = [root]

    def create_left_son(self, parent, son_value):
        son = Node()
        son.set_value(son_value)
        son.set_parent(parent)
        parent.set_left_son(son)
        self.nodes.append(son)

    def create_right_son(self, parent, son_value):
        son = Node()
        son.set_value(son_value)
        son.set_parent(parent)
        parent.set_right_son(son)
        self.nodes.append(son)
        

    
        
