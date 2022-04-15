# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import rlcompleter
from socket import if_indextoname
import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, list_board, size):
        self.list_board = list_board
        self.size = size

    def get_list(self):
        return self.list_board

    def set_list(self, x):
        self.list_board =x

    def get_size(self):
        return self.size

    def set_size(self,x):
        self.size=x

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.list_board[row + 1][col]

        pass
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if (row == 0):
            return ((self.list_board[row+1][col]),None)
        elif (row == self.size-1):
            return (None,(self.list_board[row][col]))
        else:
            print(self.list_board[row + 2][col])
            print(self.list_board[row][col])            
            return ((self.list_board[row + 2][col]),(self.list_board[row][col]))

    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        if (col == 0):
            return (None, (self.list_board[row+1][col+1]))
        elif (col == self.size-1):
            return ((self.list_board[row+1][col - 1]),None)
        else:
            return ((self.list_board[row+1][col-1]),(self.list_board[row+1][col+1]))
        pass
    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        list_board = []
        f = open(filename)
        for line in f: 
                list = []
                board_line = line.split()
                list = []
                for x in board_line:
                    list.append(int(x))
                list_board.append(list)

        bd = Board(list_board, int(list_board[0][0]))
        return bd

    # TODO: outros metodos da classe

    def to_string(self):
        aux = ""
        for x in self.list_board:
            if(x != self.list_board[- len(self.list_board)]):
                for y in x:
                    aux = aux + str(y) + "\t"
                if(x!= self.list_board[-1]):
                    aux = aux + "\n"
        return aux

class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        initial_state=NumbrixState(board)
        super().__init__(initial_state)
        pass

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        #print(any("6" in sublist for sublist in state.board.get_list()))
        ret = [] #Lista que contem tuplo (NovoNumero,X,Y)
        size = state.board.get_size()
        for i in range(state.board.get_size()):     
            for j in range(state.board.get_size()):
                if(state.board.get_number(i,j) == 0):
                    continue    
                else:
                    print("i=",i)
                    print("j=",j)
                    print( state.board.adjacent_vertical_numbers(2,1))
                    vert_adj = state.board.adjacent_vertical_numbers(i,j)
                    hori_adj = state.board.adjacent_horizontal_numbers(i,j)
        x = state.board.adjacent_vertical_numbers(2,2)
        print(x)
        
        pass

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        # TODO
        pass

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    # TODO: outros metodos da classe


if __name__ == "__main__":
    #/home/fabokitas/IA/Projeto/IA-2022/projP3-09Mar/test.txt
    bds = Board.parse_instance("/home/fabokitas/IA/Projeto/IA-2022/projP3-09Mar/test.txt")   
    """print("Initial:\n", bds.to_string(), sep="")
    print(bds.adjacent_vertical_numbers(2,2))
    print(bds.adjacent_horizontal_numbers(2,2))
    print(bds.adjacent_vertical_numbers(1,1))
    print(bds.adjacent_horizontal_numbers(1,1))
    print("Novas Cenas")"""
    problem = Numbrix(bds)
    initial_state = NumbrixState(bds)
    print(initial_state.board.get_number(2,2))
    problem.actions(initial_state)
        
    pass
