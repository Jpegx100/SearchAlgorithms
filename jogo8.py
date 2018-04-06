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


if __name__ == '__main__':
    matrix = [[1,0,3],[7,2,6],[5,4,8]]
    root = Jogo8Node(content=matrix, father=None)
    # result = root.breadth_first_search()
    # result = root.depth_first_search()
    result = root.best_first_search()
    print('Resultado::::')
    print_tree(result)