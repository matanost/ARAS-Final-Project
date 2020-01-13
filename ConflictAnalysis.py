
import Assignment
from CNF_formula import CNF_formula, Literal, Sign
import enum
import copy

class impGraph:

    class impNodesTypes(enum.Enum):
        Untyped = enum.auto()
        Root = enum.auto()
        Literal = enum.auto()
        Conflict = enum.auto()

    class impNode:

        @classmethod
        def __init__(self, node_type, literal, level):
            self.type = node_type
            self.literal = literal        
            self.level = level
            self.ingoing = []
            self.outgoing = []

        def __eq__(self,other):
            return (self.type == other.type) and (self.literal == other.literal) and (self.level == other.level) and (self.ingoing == other.ingoing) and (self.outgoing == other.outgoing)

        def __ne__(self,other):
            return not self == other

    class impEdge:
        
        @classmethod
        def __init__(self, clause, source, target):
            self.clause = clause
            self.source = source
            self.target = target
        
        @classmethod
        def __eq__(self,other):
            return (self.clause == other.clause) and (self.source == other.source) and (self.target == other.target)
                
        @classmethod
        def __ne__(self,other):
            return not self == other    
            

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
    
    def find_first_uip(graph, root):
        if not graph.conflicts:
            return None
        conflict = graph.conflicts[0]
        root_dist = is_reachable(graph, root, conflict)[1]
        first_uip = {"node":root, "dist_from_conflict" : root_dist}
        for n in graph.nodes:
            graph_copy = copy.deepcopy(graph)
            graph_copy.remove_nodes(n)
            is_r, = is_reachable(graph_copy, root, conflict)
            if not is_r:
                dist = is_reachable(graph_copy, n, conflict)[1]
                if dist < first_uip["dist_from_conflict"]:
                    first_uip = {"node":root, "dist_from_conflict" : root_dist}
        return first_uip["node"].literal

    #######################################################################
    #######################################################################                    

    def __init__(self, formula):
        self.nodes = list() 
        self.edges = list()       
        self.roots = list()
        self.lit_to_node = dict()
        self.conflicts = list()
        self.formula = formula

    def add_root(self, literal, level):
        new_node = impGraph.impNode(impGraph.impNodesTypes.Root, literal, level)
        self.nodes.append(new_node)
        self.roots.append(new_node)
        self.lit_to_node[literal] = new_node

    def add_literal(self, literal, level):
        new_node = impGraph.impNode(impGraph.impNodesTypes.Literal, literal, level)
        self.nodes.append(new_node)
        self.lit_to_node[literal] = new_node

    def add_conflict(self):
        new_node = impGraph.impNode(impGraph.impNodesTypes.Conflict, literal, level)
        self.nodes.append(new_node)
        self.conflicts.append(new_node)

    def get_node(self, literal):
        return self.lit_to_node[literal]

    def add_edge(self, source_node, clause, target_node):
        edge = impGraph.impEdge(clause, source_node, target_node)
        self.edges.append(edge)
        source_node.outgoing.append(edge)
        target_node.ingoing.append(edge)

    def remove_node(self, node):
        for e in node.outgoing():
            e.target.ingoing.remove(e)
            self.edges.remove(e)
        for e in node.ingoing():
            e.target.outgoing.remove(e)            
            self.edges.remove(e)
        self.nodes.remove(node)           

    def explain(init_clause, root):
        first_uip = find_first_uip(self, root)        
        clause = init_clause
        while -first_uip not in clause:
            #TODO find last assigned literal.
            #TODO find c' that will be called other_clause
            clause = Assignment.resolve_clauses(clause, other_clause, last_assigned_literal)          
        return clause
