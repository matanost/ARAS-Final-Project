
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
    
        def __init__(self, node_type, key, literal=None, level=None):
            self.type = node_type
            self.literal = literal        
            self.level = level
            self.key = key
            self.ingoing_key = []
            self.outgoing_key = []

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

        def __hash__(self):
            if self.type == impGraph.impNodesTypes.Literal or self.type == impGraph.impNodesTypes.Root:
                return self.literal.__hash__()
            else :
                return str.__hash__("Conflict") + self.level.__hash__()

    class impEdge:
        
        def __init__(self, clause, clause_index ,source_key, target_key): #Clause index is passed for easier debug.
            self.clause = clause
            self.clause_index = clause_index
            self.source_key = source_key
            self.target_key = target_key
            self.key = self.__str__()
        
        def __eq__(self,other):
            if not isinstance(other, impGraph.impEdge):                
                return False            
            return (self.clause == other.clause) and (self.clause_index == other.clause_index) and (self.source == other.source) and (self.target == other.target)
                
        def __ne__(self,other):
            return not self == other
            
        def __str__(self):
            return "<{},c{},{}>\n".format(str(self.source_key),str(self.clause_index),str(self.target_key))

        def __hash__(self):            
            return self.source.__hash__() + self.target.__hash__() + self.clause_index.__hash__() + self.clause.__hash__()

    @staticmethod
    def is_reachable(graph, s, t):
        if len(graph.nodes) == 0:
            return False
        stopping_depth = len(graph.nodes) + 1
        to_visit = [(s,0)]
        if t not in graph.nodes:
            raise Exception("Target not in nodes" + str(t))
        if s not in graph.nodes:
            raise Exception("Source not in nodes:" + str(s))
        while to_visit:
            node, depth = to_visit.pop(0)
            if len(graph.nodes[node].outgoing_key) == 0:
                continue
            if depth == stopping_depth:
                continue
            for edge_key in graph.nodes[node].outgoing_key:
                if graph.edges[edge_key].target_key == t:
                    return (True, depth+1)                
                to_visit.append((graph.edges[edge_key].target_key, depth + 1))
        return (False,0)
    
    @staticmethod
    def find_first_uip(graph, root_key):
        if not graph.conflicts:
            return None
        if root_key not in graph.nodes.keys():
            raise Exception("Root not in nodes: " + str(root_key))
        conflict_key = graph.conflicts[0]
        root_dist = impGraph.is_reachable(graph, root_key, conflict_key)[1]
        first_uip = {"node" : root_key, "dist_from_conflict" : root_dist}
        for n_key in graph.nodes.keys():
            if (n_key == root_key) or (n_key == conflict_key):
                continue
            graph_copy = copy.deepcopy(graph)
            graph_copy.del_node(n_key)
            is_r = impGraph.is_reachable(graph_copy, root_key, conflict_key)[0]
            if not is_r:
                dist = impGraph.is_reachable(graph, n_key, conflict_key)[1]
                if dist < first_uip["dist_from_conflict"]:
                    first_uip = {"node": n_key, "dist_from_conflict" : dist}
        return first_uip["node"]

    #=====================================================================
    #=====================================================================   

    def __init__(self, formula):
        self.nodes = dict() 
        self.edges = dict()       
        self.conflicts = list()
        self.formula = formula
        self.lit_assign_ord = list()        

    def verify_edges(self):
        edges = set()
        for e in self.edges.keys():
            if (e not in self.nodes[self.edges[e].source_key].outgoing_key) or (e not in self.nodes[self.edges[e].target_key].ingoing_key):
                raise Exception("Some node doesn't contain one of its edges")
        for n in self.nodes.values():
            for e in (n.ingoing_key + n.outgoing_key):
                edges.add(e)
        if edges != self.edges.keys():
            if len(edges) <= len(self.edges):
                raise Exception("Bad Checking at previous level")
            raise Exception("More edges at nodes in/out then in edges")
        
        
    def add_root(self, literal, level):
        self.nodes[literal] = impGraph.impNode(self.impNodesTypes.Root, key=literal, literal=literal, level=level)

    def add_literal(self, literal, level):
        self.nodes[literal] = impGraph.impNode(self.impNodesTypes.Literal, key=literal, literal=literal, level=level)

    def add_conflict(self):
        conflict_key = "Conflict" + str(len(self.conflicts))
        self.nodes[conflict_key] = impGraph.impNode(self.impNodesTypes.Conflict, conflict_key, literal=None, level=None)
        self.conflicts.append(conflict_key)

    def add_edge_internal(self, source_key, clause, target_key):
        edge = impGraph.impEdge(clause, self.formula.index(clause), source_key, target_key)
        self.edges[edge.key] = edge        
        self.nodes[source_key].outgoing_key.append(edge.key)
        self.nodes[target_key].ingoing_key.append(edge.key)
        self.verify_edges()
        
    def add_edge(self, source_lit, clause, target_lit):
        if source_lit not in self.nodes.keys():
            raise Exception("Source not in nodes " + str(source_lit))
        if target_lit not in self.nodes.keys():
            raise Exception("Target not in nodes " + str(target_lit))
        self.add_edge_internal(source_lit, clause, target_lit)        
        
    def add_edge_to_conflict(self, source_lit, clause):
        if source_lit not in self.nodes.keys():
            raise Exception("Source not in nodes " + str(source_lit))
        self.add_edge_internal(source_lit, clause, self.conflicts[-1])

    def del_node(self, node_key):
        node = self.nodes[node_key]        
        for e_key in node.outgoing_key:
            target_key = self.edges[e_key].target_key            
            self.nodes[target_key].ingoing_key.remove(e_key)            
            del self.edges[e_key]
                
        for e_key in node.ingoing_key:
            source_key = self.edges[e_key].source_key
            self.nodes[source_key].outgoing_key.remove(e_key)
            del self.edges[e_key]
            
        nodes_copy = copy.deepcopy(self.nodes)
        for key, value in nodes_copy.items():
            if value == node:
                del self.nodes[key]
        self.verify_edges()

    def del_conflicts(self):
        for conflict in self.conflicts:
            self.del_node(conflict)
        self.conflicts = list()

    def explain(self, init_clause, last_decision):
        if not last_decision:
            raise Exception("Explaining conflict on level 0")
        first_uip_key = impGraph.find_first_uip(self, root_key=last_decision)        
        clause = init_clause
        first_uip_literal = self.nodes[first_uip_key].literal
        if not first_uip_literal:
            raise Exception("None literal first UIP: " + str(first_uip_key))
        it = 0
        levels = lambda clause: [(self.nodes[l].level if l in self.nodes else self.nodes[-l].level) for l in clause]
        num_appear = lambda lvl, a : sum([(1 if lvl==elm else 0) for elm in a])
        first_uip_lvl = self.nodes[first_uip_key].level
        while not ((-first_uip_literal in clause) and ((num_appear(first_uip_lvl, levels(clause)) == 1))): 
            for lit in reversed(self.lit_assign_ord):
                if -lit in clause:
                    last_assigned_literal = lit
                    break
            if len(self.nodes[last_assigned_literal].ingoing_key) > 0:
                other_clause = self.edges[self.nodes[last_assigned_literal].ingoing_key[0]].clause
                clause = A.Assignment.resolve_clauses(clause, other_clause, last_assigned_literal)
                it += 1
            else:
                raise Exception("Node " + str(self.nodes[last_assigned_literal]) + " has no incoming edges.")
        return clause
      
    def __str__(self):
        out = "Implication Graph:\n*******\n"
        out += "Original formula={}\n".format(self.formula)
        out += "Assignments by order: \n["
        for i,l in enumerate(self.lit_assign_ord):
            out += str(l) + ("," if i < (len(self.lit_assign_ord) - 1) else "")
        out += "]\n"
        out += "Nodes:\n"      
        for l,n in self.nodes.items():        
            out += "Literal " + str(l) + " mapped to node " + str(n) + " at level " + str(n.level) + "\n"
        out += "Edges:\n"
        for e in self.edges.values():
            out += str(e)
        out += "*******\n"
        return out
