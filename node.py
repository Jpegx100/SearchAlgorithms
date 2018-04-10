from operator import attrgetter
from lxml import etree
from utils import *

class Node():

    def __init__(self, content, father):
        self.content = content
        self.father = father
        if self.father:
            self.father.children.append(self)
        self.heuristic_value = self.get_heuristic_value()
        self.children = []
    
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
    
    def best_first_search(self):
        states_frontier = [self]
        while len(states_frontier)>0:
            node = min(states_frontier, key=attrgetter('heuristic_value'))
            if node.verify_matrix():
                return node
            children = [child for child in node.expand_nodes() if not node_in_states(child, states_frontier)]
            states_frontier.extend(children)
            node.heuristic_value = 999999999
    
    def get_content(self):
        sliced = '<div>'+str(self.content).replace('], [', '<br />').replace('[', '').replace(']', '').replace(',','').replace('0', '_')+'</div>'
        return sliced
    
    def get_parsed_tree(self):
        tree = {
            "desc": self.get_content()
        }
        if self.children:
            tree["children"] = [child.get_parsed_tree() for child in self.children]
        return tree
    
    def get_parents(self, node):
        if node:
            if node.father:
                return [node.father] + self.get_parents(node.father)
            else:
                return []
    
    def create_tree(self, ul, root, best_solution):
            li = etree.SubElement(ul, 'li')
            
            if root["desc"] in best_solution:
                root["desc"] = '<div class="best">' + root["desc"][5:]
            elem = etree.fromstring(root["desc"])
            li.append(elem)
            
            if 'children' in root:
                ul = etree.SubElement(li, 'ul')
                for child in root['children']:
                    self.create_tree(ul, child, best_solution)
    
    def save_result(self, node_solution):
        best_solution = [node_solution] + self.get_parents(node_solution)
        best_solution = [bf.get_content() for bf in best_solution]

        page = etree.Element('html')
        doc = etree.ElementTree(page)
        headElt = etree.SubElement(page, 'head')
        bodyElt = etree.SubElement(page, 'body')

        link = etree.SubElement(headElt, 'link')
        link.set('rel', 'stylesheet')
        link.set('href', 'tree.css')

        title = etree.SubElement(headElt, 'title')
        title.text = 'Resolução do problema'

        div = etree.SubElement(bodyElt, "div")
        div.set("class", "tree")

        ul = etree.SubElement(div, 'ul')
        self.create_tree(ul, self.get_parsed_tree(), best_solution)

        with open('result.html', 'wb') as arq:
            result = etree.tostring(page, pretty_print=True)
            print(type(result))
            arq.write(result)
            arq.close()
        