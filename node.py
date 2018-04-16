from operator import attrgetter
from lxml import etree
from utils import *

class Node():
    VISITED = 999999999
    GULOSO = 'Guloso'
    AESTRELA = 'A-estrela'
    LARGURA = 'Largura'
    PROFUNDIDADE = 'Profundidade'

    def __init__(self, content, father):
        self.content = content
        self.father = father
        self.algorithm = None
        if self.father:
            self.father.children.append(self)
            self.algorithm = self.father.algorithm
        self.heuristic_value = self.get_heuristic_value()
        self.children = []
        self.states_frontier = [self]
        self.time = 1
        self.space = 0
    
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
    
    def get_content(self):
        raise NotImplementedError

    def greedy_search(self, repeated_states, visited_nodes, states_frontier):
        self.algorithm = Node.GULOSO
        repeated_states.append(self)
        visited_nodes.append(self)
        self.heuristic_value = Node.VISITED
        
        if self.verify_matrix():
            return self
            
        children = [child for child in self.expand_nodes() if not node_in_states(child, repeated_states)]
        children.sort(key=lambda child: child.heuristic_value)
        states_frontier.extend(children)
        for child in children:
            node = child.greedy_search(repeated_states, visited_nodes, states_frontier)
            if node:
                return node
        
        return None
    
    def breadth_first_search(self):
        self.algorithm = Node.LARGURA
        index = 0
        for node in self.states_frontier:
            if node.verify_matrix():
                return node
            children = [child for child in node.expand_nodes() if not node_in_states(child, self.states_frontier)]
            self.states_frontier.extend(children)

            self.space = max(len(self.states_frontier)-index, self.space)
            index = index + 1
            self.time = self.time + 1
    
    def depth_first_search(self):
        self.algorithm = Node.PROFUNDIDADE
        repeated_states = [self]
        while len(self.states_frontier)>0:
            node = self.states_frontier.pop()
            repeated_states.append(node)
            if node.verify_matrix():
                return node
            children = [child for child in node.expand_nodes() if not node_in_states(child, repeated_states)]
            self.states_frontier.extend(children)
            self.space = max(len(self.states_frontier), self.space)
            self.time = self.time + 1
    
    def best_first_search(self):
        self.algorithm = Node.AESTRELA
        while len(self.states_frontier)>0:
            node = min(self.states_frontier, key=attrgetter('heuristic_value'))
            if node.verify_matrix():
                return node
            children = [child for child in node.expand_nodes() if not node_in_states(child, self.states_frontier)]
            self.states_frontier.extend(children)
            node.heuristic_value = Node.VISITED

            not_visited_states = [state for state in self.states_frontier if state.heuristic_value != Node.VISITED]
            self.space = max(len(not_visited_states), self.space)
            self.time = self.time + 1
    
    def get_parents(self, node):
        if node:
            if node.father:
                return [node.father] + self.get_parents(node.father)
            else:
                return []
    
    def create_tree(self, ul, best_solution):
            li = etree.SubElement(ul, 'li')
            
            if self in best_solution:
                content = self.get_content()
                index = content.index('>') + 1
                desc = '<div class="best">' + content[index:]
            else:
                desc = self.get_content()

            elem = etree.fromstring(desc)
            li.append(elem)
            
            if self.children:
                ul = etree.SubElement(li, 'ul')
                for child in self.children:
                    child.create_tree(ul, best_solution)
    
    def save_result(self, node_solution):
        best_solution = [node_solution] + self.get_parents(node_solution)

        page = etree.Element('html')
        doc = etree.ElementTree(page)
        headElt = etree.SubElement(page, 'head')
        bodyElt = etree.SubElement(page, 'body')

        link = etree.SubElement(headElt, 'link')
        link.set('rel', 'stylesheet')
        link.set('href', 'tree.css')

        title = etree.SubElement(headElt, 'title')
        title.text = 'Resolução do problema'

        h1 = etree.SubElement(bodyElt, "h1")
        h1.set("class", "title")
        
        h1.text = 'Método de busca: '+self.algorithm+' | Número máximo de nós na memória: '+str(self.space) + \
                    ' | Nós visitados: '+str(self.time)

        div = etree.SubElement(bodyElt, "div")
        div.set("class", "tree")  

        ul = etree.SubElement(div, 'ul')
        self.create_tree(ul, best_solution)

        with open('result.html', 'wb') as arq:
            result = etree.tostring(page, pretty_print=True)
            print(type(result))
            arq.write(result)
            arq.close()
        