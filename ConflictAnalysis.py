
import Assignment as A
from CNF_formula import CNF_formula, Literal, Sign, Clause
import enum
import copy

        
class impGraph:

    class impNodesTypes(enum.Enum):
        Untyped = enum.auto()
        Root = enum.auto()
        Literal = enum.auto()
        Conflict = enum.auto()


    class impNode:
    
        def __init__(self, node_type, literal=None, level=None):
            self.type = node_type
            self.literal = literal        
            self.level = level
            self.ingoing = []
            self.outgoing = []

        def __eq__(self,other):
            if not isinstance(other, impGraph.impNode):
                return False
            return (self.type == other.type) and (self.literal == other.literal) and (self.level == other.level)

        def __ne__(self,other):
            return not self == other
    
        def __str__(self):
            if self.type == impGraph.impNodesTypes.Literal:
                return str(self.literal) + ":" + str(self.level)
            elif self.type == impGraph.impNodesTypes.Root:
                return "Root|" + str(self.literal) + ":" + str(self.level)
            elif self.type == impGraph.impNodesTypes.Conflict:
                return "Conflict"

    class impEdge:
        
        def __init__(self, clause, clause_index ,source, target): #Clause index is passed for easier debug.
            self.clause = clause
            self.clause_index = clause_index
            self.source = source
            self.target = target
        
        def __eq__(self,other):
            if not isinstance(other, impGraph.impEdge):                
                return False            
            return (self.clause == other.clause) and (self.clause_index == other.clause_index) and (self.source == other.source) and (self.target == other.target)
                
        def __ne__(self,other):
            return not self == other
            
        def __str__(self):
            return "<{},c{},{}>\n".format(str(self.source),str(self.clause_index+1),str(self.target))
            
    '''@staticmethod
    def is_acyclic(graph):
        if len(graph.nodes) == 0:
            return True
        stopping_depth = len(graph.nodes) + 1
        #visited = set()
        to_visit = [(r,0) for r in graph.roots]
        while to_visit:
            node, depth = to_visit.pop(0)
            if len(node.outgoing()) == 0:
                continue
            if depth == stopping_depth:
                return False
            #visited.add(node)
            for edge in node.outgoing():
                to_visit.append((edge.target, depth + 1))
        return True'''

    @staticmethod
    def is_reachable(graph, s, t):
        if len(graph.nodes) == 0:
            return False
        stopping_depth = len(graph.nodes) + 1
        #visited = set()
        to_visit = [(s,0)]
        while to_visit:
            node, depth = to_visit.pop(0)
            if len(node.outgoing) == 0:
                continue
            if depth == stopping_depth:
                continue
            #visited.add(node)
            for edge in node.outgoing:
                if edge.target == t:
                    return (True, depth+1)
                to_visit.append((edge.target, depth + 1))
        return (False,0)
    
    @staticmethod
    def find_first_uip(graph, root):
        if not graph.conflicts:
            return None
        conflict = graph.conflicts[0]
        root_dist = impGraph.is_reachable(graph, root, conflict)[1]
        first_uip = {"node":root, "dist_from_conflict" : root_dist}
        for n in graph.nodes.values():
            graph_copy = copy.deepcopy(graph)
            graph_copy.remove_node(n)
            is_r = impGraph.is_reachable(graph_copy, root, conflict)[0]
            if not is_r:
                dist = impGraph.is_reachable(graph_copy, n, conflict)[1]
                if dist < first_uip["dist_from_conflict"]:
                    first_uip = {"node":root, "dist_from_conflict" : root_dist}
        return first_uip["node"].literal

    #######################################################################
    #######################################################################                    

    def __init__(self, formula):
        self.nodes = dict() 
        self.edges = list()       
        #self.roots = list()
        self.conflicts = list()
        self.formula = formula
        self.literal_assignments_ordered = list()        

    def add_root(self, literal, level):
        self.nodes[literal] = impGraph.impNode(self.impNodesTypes.Root, literal=literal, level=level)
        #self.roots.append(new_node)

    def add_literal(self, literal, level):
        self.nodes[literal] = impGraph.impNode(self.impNodesTypes.Literal, literal=literal, level=level)

    def add_conflict(self):
        conflict_key = "Conflict" + str(len(self.conflicts))
        self.nodes[conflict_key] = impGraph.impNode(self.impNodesTypes.Conflict)
        self.conflicts.append(conflict_key)

    def add_edge_internal(self, source_key, clause, target_key):
        edge = impGraph.impEdge(clause, self.formula.index(clause), self.nodes[source_key], self.nodes[target_key])
        self.edges.append(edge)        
        #print("Trying to add " + str(edge))
        #print("Check before ingoing assignment for n=" + str(target_key))        
        #for e in self.nodes[target_key].ingoing:
        #    print("in" + str(e))
        #print("Check after outgoing assignment for n=" + str(source_key))                       
        #for e in self.nodes[source_key].outgoing:
        #    print("out " + str(e))        
        self.nodes[source_key].outgoing.append(edge)
        self.nodes[target_key].ingoing.append(edge)
        #print("Check after ingoing assignment for n=" + str(target_key))
        #for e in self.nodes[target_key].ingoing:
        #    print("in " + str(e))
        #print("Check after outgoing assignment for n=" + str(source_key))           
        #for e in self.nodes[source_key].outgoing:
        #    print("out " + str(e))
        
    def add_edge(self, source_lit, clause, target_lit):
        self.add_edge_internal(source_lit, clause, target_lit)        
        
    def add_edge_to_conflict(self, source_lit, clause):
        self.add_edge_internal(source_lit, clause, self.conflicts[-1])

    def remove_node(self, node): #TODO this is not set yet.
        for e in node.outgoing:                        
            e.target.ingoing.remove(e)
            self.edges.remove(e)
        for e in node.ingoing:           
            e.source.outgoing.remove(e)         
            self.edges.remove(e)
        nodes_copy = copy.deepcopy(self.nodes)
        for key, value in nodes_copy.items():
            if value == node:
                del self.nodes[key]

    def remove_conflicts(self):
        for conflict in self.conflicts:
            self.remove_node(self.nodes[conflict])
        self.conflicts = list()

    def explain(self, init_clause, last_decision):
        #print("in explain")        
        if not last_decision:
            raise Exception("Explaining conflict on level 0")
        root = self.nodes[last_decision]
        first_uip = impGraph.find_first_uip(self, root)        
        clause = init_clause
        #print(clause)
        #print(self)

        #print("First UIP is " + str(first_uip))
        
        while -first_uip not in clause:
            for lit in reversed(self.literal_assignments_ordered):
                if -lit in clause:
                    last_assigned_lit = lit
                    break
            #print(last_assigned_lit)
            #print(self.nodes[last_assigned_lit].ingoing)
            if self.nodes[last_assigned_lit].ingoing:
                other_clause = self.nodes[last_assigned_lit].ingoing[0].clause
                clause = A.Assignment.resolve_clauses(clause, other_clause, last_assigned_literal)        
            else:
                raise Exception("Node has no incoming edges.")
        return clause
      
    def __str__(self):
        out = "Implication Graph:\n*******\n"
        out += "Original formula={}\n".format(self.formula)
        out += "Assignments by order: \n["
        for i,l in enumerate(self.literal_assignments_ordered):
            out += str(l) + ("," if i < (len(self.literal_assignments_ordered) - 1) else "")
        out += "]\n"
        out += "Nodes:\n"      
        for l,n in self.nodes.items():
            out += "literal " + str(l) + " mapped to node " + str(n) + "\n"
        out += "Edges:\n"
        for e in self.edges:
            out += str(e)
        out += "*******\n"
        return out
