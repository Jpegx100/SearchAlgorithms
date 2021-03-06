import click
from node import Node
from utils import *


class NRainhasNode(Node):

    def heuristic(self):
        return len(self.get_attacked_coords()) - 2*self.depth()
    
    def expand_nodes(self):
        tam = len(self.content)
        
        matrix = self.content
        matrixes = []
        attacked_coords = self.get_attacked_coords()

        for i in range(tam):
            for j in range(tam):
                if ((i, j) not in attacked_coords) and (matrix[i][j] != 1):
                    mat = copy_matrix(matrix)
                    mat[i][j] = 1
                    node = NRainhasNode(content=mat, father=self)
                    matrixes.append(node)
        
        return matrixes
    
    def get_content(self):
        heu = ''
        classe = ''
        if self.algorithm in [Node.AESTRELA, Node.GULOSO]:
            if self.heuristic_value == Node.VISITED:
                classe = 'class="visited"'
            heu = 'H = '+str(self.get_heuristic_value())

        sliced = str(self.content).replace('[[', '<tr><td>') \
                                    .replace(']]','</td></tr>') \
                                    .replace('],', '</td></tr>') \
                                    .replace('[', '<tr><td>') \
                                    .replace(',','</td><td>') \
                                    .replace('0', '') \
                                    .replace('1', '♛')
        content = '<div '+classe+'>'+heu+'<table>'+sliced+'</table></div>'
        return content
    
    def get_queens_coord(self):
        queens_coord = []
        
        for i in range(len(self.content)):
            for j in range(len(self.content)):
                if self.content[i][j] == 1:
                    queens_coord.append((i, j))
        
        return queens_coord
    
    def get_attacked_coords(self):
        tam = len(self.content)
        queens_coords = self.get_queens_coord()
        attack_coords = set([])

        for (i, j) in queens_coords:
            coords_row = [(i, column) for column in range(tam) if column!=j]
            coords_column = [(row, j) for row in range(tam) if row!=i]

            attack_coords.update(coords_row)
            attack_coords.update(coords_column)
            
            min_diag_1 = min(i, j)
            row = i - min_diag_1
            column = j - min_diag_1
            
            while row<tam and column<tam:
                if row != i and column != j:
                    attack_coords.add((row, column))
                row += 1
                column += 1
            
            min_diag_2 = min(j, tam - i - 1)
            row = i + min_diag_2
            column = j - min_diag_2

            while row>=0 and column<tam:
                if row != i and column != j:
                    attack_coords.add((row, column))
                row -= 1
                column += 1
        
        return attack_coords
    
    def count_queens(self):
        return len(self.get_queens_coord())

    def verify_matrix(self):
        queens_coords = self.get_queens_coord()
        attack_coords = self.get_attacked_coords()
        attacked_queens = [coord for coord in queens_coords if coord in attack_coords]

        return len(attacked_queens) == 0 and self.count_queens() == len(self.content)


@click.command()
@click.option('--rainhas', default=4, type=click.INT, help='Número de rainhas para o problema')
@click.option('--busca', default='a-estrela', type=click.Choice(['profundidade', 'largura', 'a-estrela', 'guloso']), help='Tipo de algorítmo de busca a ser utilizado')
def nrainhas(rainhas, busca):
    matrix = []
    for i in range(rainhas):
        matrix.append([0 for j in range(rainhas)])
    root = NRainhasNode(content=matrix, father=None)
    
    if busca == 'profundidade':
        result = root.depth_first_search()
    elif busca == 'largura':
        result = root.breadth_first_search()
    elif busca == 'guloso':
        repeated_states = []
        visited_nodes = []
        states_frontier = []
        result = root.greedy_search(repeated_states, visited_nodes, states_frontier)
        root.time = len(visited_nodes)
        root.space = len(states_frontier)
    else:
        result = root.best_first_search()

    root.save_result(result)

if __name__ == '__main__':
    nrainhas()