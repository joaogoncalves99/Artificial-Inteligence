# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 037:
# 93918 João Gonçalves
# 95571 Fábio Jerónimo

import datetime
import _pickle as pickle
from operator import truediv
import rlcompleter
from socket import if_indextoname
import sys
from unicodedata import numeric
from numpy import true_divide
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search, InstrumentedProblem,compare_searchers


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

    def __init__(self, list_board, size, new_number):
        self.list_board = list_board
        self.size = size
        self.new_number = new_number
        self.empty_spaces = 0


    def get_list(self):
        return self.list_board

    def set_list(self, x):
        self.list_board =x

    def get_size(self):
        return self.size

    def set_size(self,x):
        self.size=x
    
    def set_new_number(self,x):
        self.new_number=x

    def get_new_number(self):
        return self.new_number

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.list_board[row + 1][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if (row == 0):
            return ((self.list_board[row+2][col]),None)
        elif (row == self.size-1):
            return (None,(self.list_board[row][col]))
        else:           
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

        bd = Board(list_board, int(list_board[0][0]), None)
        return bd

    def test_board(self, number, row, col):
        size = self.get_size()
        adj = []
        adj.append(self.adjacent_vertical_numbers(row,col)[0])
        adj.append(self.adjacent_vertical_numbers(row,col)[1])
        adj.append(self.adjacent_horizontal_numbers(row,col)[0])
        adj.append(self.adjacent_horizontal_numbers(row,col)[1])
        if (adj.count(0) == 1):
            if not(number == 1 or number == size * size):
                if not(self.is_on_list(number+1,adj) or self.is_on_list(number-1,adj)):
                    return False
        if (adj.count(0) == 0):
            if (number == 1):
                if not(self.is_on_list(number+1,adj)):
                    return False
            elif (number == size * size):
                if not(self.is_on_list(number-1,adj)):
                    return False
            else:
                if not(self.is_on_list(number-1,adj) and self.is_on_list(number+1,adj)):
                    return False
        return True

    def is_on_list(self, number,list):
        for x in list:
            if (number == x):
                return True
        return False

    def to_string(self):
        aux = ""
        for x in self.list_board:
            if(x != self.list_board[- len(self.list_board)]):
                for y in x:
                    aux = aux + str(y) + "\t"
                if(x!= self.list_board[-1]):
                    aux = aux[:-1] + "\n"
        return aux[:-1]

class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        initial_state = NumbrixState(board)
        super().__init__(initial_state)
        pass

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        #get present numbers in this state
        present_numbers = []
        ret = [] #Lista que contem tuplo (NovoNumero,X,Y)
        size = state.board.get_size()
        lowest = size*size + 1
        coords_lowest = (size+1,size +1)
        free_vert = []
        free_hori = []

        #Verify if the current board is solvable; if it's not, 
        # immediately return empty ret so we don't get more actions
        for i in range(state.board.get_size()):
            for j in range(state.board.get_size()):
                current = state.board.get_number(i,j)
                if (current!=0):
                    present_numbers.append(current)
                    #we only need to check the area surrounding the number we just put on the board
                    if (current == state.board.get_new_number()):
                        if (state.board.adjacent_vertical_numbers(i,j)[0] != 0 and 
                            state.board.adjacent_vertical_numbers(i,j)[0] != None):
                            if not (state.board.test_board(state.board.adjacent_vertical_numbers(i,j)[0],i+1,j)):
                                return ret
                        if (state.board.adjacent_vertical_numbers(i,j)[1] != 0 and 
                            state.board.adjacent_vertical_numbers(i,j)[1] != None):
                            if not (state.board.test_board(state.board.adjacent_vertical_numbers(i,j)[1],i-1,j)):
                                return ret
                        if (state.board.adjacent_horizontal_numbers(i,j)[0] != 0 
                            and state.board.adjacent_horizontal_numbers(i,j)[0] != None):
                            if not (state.board.test_board(state.board.adjacent_horizontal_numbers(i,j)[0],i,j-1)):
                                return ret
                        if (state.board.adjacent_horizontal_numbers(i,j)[1] != 0 
                            and state.board.adjacent_horizontal_numbers(i,j)[1] != None):
                            if not (state.board.test_board(state.board.adjacent_horizontal_numbers(i,j)[1],i,j+1)):
                                return ret

        present_numbers.sort()
        #Find the lowest number on Board and the coords of it
        for i in range(state.board.get_size()):
            for j in range(state.board.get_size()):
                if state.board.get_number(i,j) == present_numbers[0]:
                    lowest = present_numbers[0]
                    coords_lowest = (i,j)
                    break
            else:
                continue
            break
        
        vert_adj = state.board.adjacent_vertical_numbers(coords_lowest[0],coords_lowest[1])
        if (vert_adj[0] == 0):
            free_vert.append((coords_lowest[0]+1,coords_lowest[1]))
        if (vert_adj[1] == 0):
            free_vert.append((coords_lowest[0]-1,coords_lowest[1]))
        hori_adj = state.board.adjacent_horizontal_numbers(coords_lowest[0],coords_lowest[1])
        if (hori_adj[0] == 0):
            free_hori.append((coords_lowest[0],coords_lowest[1]-1))
        if (hori_adj[1] == 0):
            free_hori.append((coords_lowest[0],coords_lowest[1]+1))
        free_coord = free_hori+free_vert

        #Se o lowest n for um anda até ao 1
        if(lowest != 1):
            current = lowest
            if (not(self.is_on_list(current - 1, present_numbers))):
                #else checks if there is a free spot for the number above
                for coord in free_coord:
                    #checks if the number above is already adjacent to the position we're checking
                    if (current>2):
                        if (self.is_on_list(0,state.board.adjacent_vertical_numbers(coord[0],coord[1])) or 
                            self.is_on_list(0,state.board.adjacent_horizontal_numbers(coord[0],coord[1]))):
                            ret.append((coord[0], coord[1],current-1))
                    else:
                        ret.append((coord[0], coord[1],current-1))
        else:
            for i in range(1, size*size):
                if not(i in present_numbers):
                    break
                current = present_numbers[i-1]

            distance = 0
            if not(current == present_numbers[-1]):
                upper = present_numbers[i-1]
                distance = upper - (current+1)
                flag_1=False
                flag_2=False
                for i in range(state.board.get_size()):     
                    for j in range(state.board.get_size()):
                        if state.board.get_number(i,j) == current:
                            coords_lowest = (i,j)
                            flag_1=True
                        if state.board.get_number(i,j) == upper:
                            coords_upper = (i,j)
                            flag_2=True
                    if (flag_1 and flag_2):
                        break

            else:
                for i in range(state.board.get_size()):     
                    for j in range(state.board.get_size()):
                        if state.board.get_number(i,j) == current:
                            coords_lowest = (i,j)
                            break
                    else:
                        continue
                    break
                    
            if (current!=lowest):
                free_vert = []
                free_hori = []
                vert_adj = state.board.adjacent_vertical_numbers(coords_lowest[0],coords_lowest[1])
                if (vert_adj[0] == 0):
                    free_vert.append((coords_lowest[0]+1,coords_lowest[1]))
                if (vert_adj[1] == 0):
                    free_vert.append((coords_lowest[0]-1,coords_lowest[1]))
                hori_adj = state.board.adjacent_horizontal_numbers(coords_lowest[0],coords_lowest[1])
                if (hori_adj[0] == 0):
                    free_hori.append((coords_lowest[0],coords_lowest[1]-1))
                if (hori_adj[1] == 0):
                        free_hori.append((coords_lowest[0],coords_lowest[1]+1))
                free_coord = free_hori+free_vert 

            #checks if the number immediately above current is present on the board
            if (current<size*size):
                if (not(self.is_on_list(current+1, present_numbers))):
                    flag = False
                    if ((current<size*size-1) and (self.is_on_list(current + 2,present_numbers))):
                        flag = True
                        for coord in free_coord:
                            #checks if the number above is already adjacent to the position we're checking
                            if (self.is_on_list(current+2,state.board.adjacent_vertical_numbers(coord[0],coord[1])) or 
                                self.is_on_list(current+2,state.board.adjacent_horizontal_numbers(coord[0],coord[1]))):
                                ret.append(( coord[0], coord[1], current+1))
                        
                    if (not(flag)):
                        #else checks if there is a free spot for the number above
                        for coord in free_coord:
                            #checks if the number above is already adjacent to the position we're checking
                            if (current<size*size-1 and current != present_numbers[-1]):
                                if (self.is_on_list(0,state.board.adjacent_vertical_numbers(coord[0],coord[1])) or 
                                    self.is_on_list(0,state.board.adjacent_horizontal_numbers(coord[0],coord[1]))):
                                    man_dist=(abs(coord[0]-coords_upper[0])+abs(coord[1]-coords_upper[1]))
                                    if not(man_dist>distance):
                                        ret.append((coord[0], coord[1],current+1))
                            elif (current<size*size-1):
                                if (self.is_on_list(0,state.board.adjacent_vertical_numbers(coord[0],coord[1])) or 
                                    self.is_on_list(0,state.board.adjacent_horizontal_numbers(coord[0],coord[1]))):
                                        ret.append((coord[0], coord[1],current+1))
                            else:
                                ret.append((coord[0], coord[1],current+1))
        return ret

    

    def is_on_list(self, number,list):
        for x in list:
            if (number == x):
                return True
        return False

    def get_present(self, state: NumbrixState):
        #returns present numbers in state
        number_list = []
        for i in range(state.board.get_size()):     
            for j in range(state.board.get_size()):
                if(state.board.get_number(i,j) != 0):
                    number_list.append(state.board.get_number(i,j))
        return number_list
        
    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        #Action (x,y,novo_numero))
        size = state.board.get_size()
        x = action[0]
        y = action[1]  
        new_number = action[2]
        state_new = pickle.loads(pickle.dumps(state,-1))
        
        for i in range(size):
            for j in range(size):
                if((i == x) and j == y):
                    state_new.board.get_list()[i + 1][j] = new_number
                    state_new.board.set_new_number(new_number)

        adj_numbers = state.board.adjacent_horizontal_numbers(x,y) + state.board.adjacent_vertical_numbers(x,y)
 
        if(adj_numbers.count(0) == 0):
            state_new.board.empty_spaces += -4
        elif(adj_numbers.count(0) == 1):
            state_new.board.empty_spaces += -2 + adj_numbers.count(None)
        elif(adj_numbers.count(0) == 2):
            state_new.board.empty_spaces += 0 + adj_numbers.count(None)
        elif(adj_numbers.count(0) == 3):
            state_new.board.empty_spaces += 2 + adj_numbers.count(None)
        elif(adj_numbers.count(0) == 4):
            state_new.board.empty_spaces += 4 

        return state_new

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        aux = []
        adj=[]
        size = state.board.get_size()
        max = size**2
        for i in range(size):
            for j in range(size):
                number = state.board.get_number(i,j)
                vert_adj_lower = state.board.adjacent_vertical_numbers(i,j)[0]
                hori_adj_left = state.board.adjacent_horizontal_numbers(i,j)[0]
                vert_adj_upper = state.board.adjacent_vertical_numbers(i,j)[1]
                hori_adj_right = state.board.adjacent_horizontal_numbers(i,j)[1]
                lower = number - 1
                upper = number + 1
                adj = [vert_adj_lower,vert_adj_upper,hori_adj_left,hori_adj_right]
                if(number == 0):
                    return False
                if((number == max and not(lower in adj)) or (number == 1 and not(upper in adj)) or 
                    ((max > number > 1)and not(lower in adj and upper in adj))):
                    return False
                if number in aux:
                    return False
                aux.append(number)
        return True
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        return node.state.board.empty_spaces
        pass

if __name__ == "__main__":
    filename=sys.argv[1]
    board = Board.parse_instance(filename)
    problem= Numbrix(board)
    goal_node = depth_first_tree_search(problem)
  
    print(goal_node.state.board.to_string())
    pass
   