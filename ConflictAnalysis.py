
import Assignment
import enum
import copy

class impNodesTypes(enum.Enum):
    Untyped    
    Root
    Literal
    Conflict
    
class impNode:

    @classmethod
    def __init__(self,type, literal, level):
        self.type = type
        self.literal = literal        
        self.level = level
        self.ingoing = []
        self.outgoing = []

    def __eq__(self,other):
        return (self.type == other.type) and
               (self.literal == other.literal) and
               (self.level == other.level) and
               (self.ingoing == other.ingoing) and           
               (self.outgoing == other.outgoing)

    def __ne__(self,other):
        return not self == other
           
class impEdge:

    @classmethod
    def __init__(self, clause, source, target):
        self.clause = clause
        self.source = source
        self.target = target
 
    def __eq__(self,other):
        return (self.clause == other.clause) and
               (self.source == other.source) and
               (self.target == other.target)

    def __ne__(self,other):
        return not self == other       

class imgGraph:

    def is_acyclic(graph):
        if len(graph.nodes) == 0:
            return True
        stopping_depth = len(graph.nodes) + 1
        visited = set()
        to_visit = [(r,0) for r in graph.roots]
        while to_visit:
            node, depth = to_visit.pop(0)
            if len(node.outgoing()) == 0:
                continue
            if depth == stopping_depth:
                return False
            visited.add(node)
            for edge in node.outgoing():
                to_visit.append((edge.target, depth + 1))
        return True

    def is_reachable(graph, s, t):
        if len(graph.nodes) == 0:
            return False
        stopping_depth = len(graph.nodes) + 1
        visited = set()
        to_visit = [(s,0)]
        while to_visit:
            node, depth = to_visit.pop(0)
            if len(node.outgoing()) == 0:
                continue
            if depth == stopping_depth:
                continue
            visited.add(node)
            for edge in node.outgoing():
                if edge.target == t:
                    return (True, depth+1)
                to_visit.append((edge.target, depth + 1))
        return (False,0)
    
    def find_uip(graph, root):
        if not graph.conflicts:
            return None
        conflict = graph.conflicts[0]
        , root_dist = is_reachable(graph, root, conflict)
        uip = (root, root_dist)
        for n in graph.nodes:
            graph_copy = copy.deepcopy(graph)
            graph_copy.remove_nodes(n)
            is_r, = is_reachable(graph_copy, root, conflict)
            if !is_r:
                , dist = is_reachable(graph_copy, n, conflict)
                if dist < root_dist:
                    uip = (n, dist)        

    def __init__(self):
        self.nodes = set() 
        self.edges = set()       
        self.roots = list()
        self.lit_to_node = dict()
        self.conflicts = list()

    def add_root(literal, level):
        new_node = impNode(impNodesTypes.Root, literal, level)
        self.nodes.add(new_node)
        self.roots.append(new_node)
        self.lit_to_node[literal] = new_node

    def add_literal(literal, level)
        new_node = impNode(impNodesTypes.Literal, literal, level)
        self.nodes.add(new_node)
        self.lit_to_node[literal] = new_node

    def add_conflict():
        new_node = impNode(impNodesTypes.Conflict, literal, level)
        self.nodes.add(new_node)
        self.conflicts.append(new_node)

    def get_node(literal):
        return self.lit_to_node[literal]

    def add_edge(source_node, clause, target_node):
        edge = impEdge(clause, source_node, target_node)
        self.edges.add(edge)
        source_node.outgoing.append(edge)
        target_node.ingoing.append(edge)

    def remove_node(self,node):
        for e in node.outgoing():
            e.target.ingoing.remove(e)
            self.edges.remove(e)
        for e in node.ingoing():
            e.target.outgoing.remove(e)            
            self.edges.remove(e)
        self.nodes.remove(node):            

    def explain(clause):
