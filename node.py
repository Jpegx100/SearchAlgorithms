from operator import attrgetter
from utils import *

class Node():

    def __init__(self, content, father):
        self.content = content
        self.father = father
        self.heuristic_value = self.get_heuristic_value()
    
    def get_heuristic_value(self):
        return self.depth() + self.heuristic()
    
    def depth(self):
        if self.father:
            return 1 + self.father.depth()
        return 0
    
    def heuristic(self):
        raise NotImplementedError

    def expand_nodes(self):
        raise NotImplementedError

    def verify_matrix(self):
        raise NotImplementedError
    
    def breadth_first_search(self):
        states_frontier = [self]
        for node in states_frontier:
            if node.verify_matrix():
                return node
            children = [child for child in node.expand_nodes() if not node_in_states(child, states_frontier)]
            states_frontier.extend(children)
            print('------FRONTEIRA DE ESTADOS------')
            print_states(states_frontier)
    
    def depth_first_search(self):
        states_frontier = [self]
        repeated_states = [self]
        while len(states_frontier)>0:
            node = states_frontier.pop()
            repeated_states.append(node)
            if node.verify_matrix():
                return node
            children = [child for child in node.expand_nodes() if not node_in_states(child, repeated_states)]
            states_frontier.extend(children)
            print('------FRONTEIRA DE ESTADOS------')
            print_states(states_frontier)
    
    def best_first_search(self):
        states_frontier = [self]
        while len(states_frontier)>0:
            node = min(states_frontier, key=attrgetter('heuristic_value'))
            if node.verify_matrix():
                return node
            children = [child for child in node.expand_nodes() if not node_in_states(child, states_frontier)]
            states_frontier.extend(children)
            print('------FRONTEIRA DE ESTADOS------')
            print_states(states_frontier, show_attrs=True)
            node.heuristic_value = 999999999