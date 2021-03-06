import click
from utils import *
from node import Node

class Jogo8Node(Node):
    
    def heuristic(self):
        total_distance = 0

        result = {
            1: (0,0),
            2: (0,1),
            3: (0,2),
            4: (1,0),
            5: (1,1),
            6: (1,2),
            7: (2,0),
            8: (2,1),
            0: (2,2)
        }
        
        for real_row in range(3):
            for real_column in range(3):
                value = self.content[real_row][real_column]
                expected_row, expected_column = result[value]
                total_distance += abs(real_row - expected_row) + \
                                  abs(real_column - expected_column)
        
        return total_distance
    
    def get_content(self):
        heu = ''
        classe = ''
        if self.algorithm in [Node.AESTRELA, Node.GULOSO]:
            if self.heuristic_value == Node.VISITED:
                classe = 'class="visited"'
            heu = 'H = '+str(self.get_heuristic_value())

        sliced = str(self.content).replace(' ', '') \
                                    .replace('[[', '<tr><td class="j8">') \
                                    .replace(']]','</td></tr>') \
                                    .replace('],', '</td></tr>') \
                                    .replace('[', '<tr><td class="j8">') \
                                    .replace(',','</td><td class="j8">') \
                                    .replace('0', '') \
                                    .replace('<td class="j8"></td>', '<td class="empty"></td>')
        content = '<div '+classe+'>'+heu+'<table>'+sliced+'</table></div>'
        return content
    
    def expand_nodes(self):
        matrix = self.content
        matrixes = []
        for i in range(3):
            for j in range(3):
                if matrix[i][j] == 0:

                    if i>0:
                        mat = copy_matrix(matrix)
                        mat[i][j], mat[i-1][j] = mat[i-1][j], mat[i][j]
                        node = Jogo8Node(content=mat, father=self)
                        matrixes.append(node)
                    
                    if i<2:
                        mat = copy_matrix(matrix)                    
                        mat[i][j], mat[i+1][j] = mat[i+1][j], mat[i][j]
                        node = Jogo8Node(content=mat, father=self)
                        matrixes.append(node)
                    
                    if j>0:
                        mat = copy_matrix(matrix)                    
                        mat[i][j], mat[i][j-1] = mat[i][j-1], mat[i][j]
                        node = Jogo8Node(content=mat, father=self)
                        matrixes.append(node)
                    
                    if j<2:
                        mat = copy_matrix(matrix)                    
                        mat[i][j], mat[i][j+1] = mat[i][j+1], mat[i][j]
                        node = Jogo8Node(content=mat, father=self)
                        matrixes.append(node)
        
        return matrixes
    
    def verify_matrix(self):
        matrix = self.content
        equals = matrix[0] == [1,2,3] and \
                matrix[1] == [4,5,6] and \
                matrix[2] == [7,8,0]
        return equals


@click.command()
@click.option('--tabuleiro', default='103425786', help='Tabuleiro inicial contendo todos os números entre 0 e 8 sem repeticao(Ex:103726548)')
@click.option('--busca', default='a-estrela', type=click.Choice(['profundidade', 'largura', 'a-estrela', 'guloso']), help='Tipo de algorítmo de busca a ser utilizado')
def jogo_8(tabuleiro, busca):
    
    if len(tabuleiro)!=9:
        print('Tabuleiro em formato incorreto')
        return

    a,b,c,d,e,f,g,h,i = tabuleiro
    matrix = [[int(a),int(b),int(c)],[int(d),int(e),int(f)],[int(g),int(h),int(i)]]

    root = Jogo8Node(content=matrix, father=None)
    
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
    jogo_8()
    print('Concluído')