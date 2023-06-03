# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 162:
# 96556 Miguel Moreira
# 95657 Pedro Almeida

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

def better_lower(value):     #esta função vai ignorar None, ao contrário da função lower

    if value != None:
        result = value.lower()

    else:
        result = value

    return result

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
de abertos nas procuras informadas. """
        return self.id < other.id
    

    


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, grid, ROW_counts, COL_counts):
        self.grid = grid
        self.ROW_counts = ROW_counts
        self.COL_counts = COL_counts

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        
        return self.grid[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""

        if row == 0:
            return (None, self.grid[row+1][col])
        
        elif row == 9:
            return (self.grid[row-1][col], None)
        
        else:
            return self.grid[row-1][col], self.grid[row+1][col]

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if col == 0:
            return (None, self.grid[row][col+1])
        
        elif col == 9:
            return (self.grid[row][col-1], None)
        
        else:
            return self.grid[row][col-1], self.grid[row][col+1]
        
    def adjacent_diagonal_values(self, row: int, col: int):

        if self.is_upper_left(row, col):
            return None, None, None, self.grid[row+1][col+1]
        
        elif self.is_upper_right(row, col):
            return None, None, self.grid[row+1][col-1], None
        
        elif self.is_lower_left(row, col):
            return None, self.grid[row-1][col+1], None, None
        
        elif self.is_lower_right(row, col):
            return self.grid[row-1][col-1], None, None, None
        
        elif self.is_upper_middle(row, col):
            return None, None, self.grid[row+1][col-1], self.grid[row+1][col+1]
        
        elif self.is_lower_middle(row, col):
            return self.grid[row-1][col-1], self.grid[row-1][col+1], None, None
        
        elif self.is_left_middle(row, col):
            return None, self.grid[row-1][col+1], None, self.grid[row+1][col+1]
        
        elif self.is_right_middle(row, col):
            return self.grid[row-1][col-1], None, self.grid[row+1][col-1], None
        
        else:
            return self.grid[row-1][col-1], self.grid[row-1][col+1], self.grid[row+1][col-1], self.grid[row+1][col+1]

    def is_upper_left(self, row: int, col: int):
        return row == 0 and col == 0
    
    def is_upper_right(self, row: int, col: int):
        return row == 0 and col == 9
    
    def is_lower_left(self, row: int, col: int):
        return row == 9 and col == 0
    
    def is_lower_right(self, row: int, col: int):
        return row == 9 and col == 9

    def is_upper_middle(self, row: int, col: int):
        return row == 0 and col != 0 and col != 9
    
    def is_lower_middle(self, row: int, col: int):
        return row == 9 and col != 0 and col != 9
    
    def is_left_middle(self, row: int, col: int):
        return col == 0 and row != 0 and row != 9
    
    def is_right_middle(self, row: int, col: int):
        return col == 9 and row != 0 and row != 9
        
    def is_water_around_boat1(self, row: int, col: int):
        
        above, below = self.adjacent_vertical_values(row, col)
        left, right = self.adjacent_horizontal_values(row, col)
        upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col)
        
        """left = better_lower(left)
        right = better_lower(right)
        above = better_lower(above)
        below = better_lower(below)
        upper_left = better_lower(upper_left)
        upper_right = better_lower(upper_right)
        lower_left = better_lower(lower_left)
        lower_right = better_lower(lower_right)"""

        if left == "." or right == "." or above == "." or below == "." or upper_left == "." or upper_right == "." or lower_left == "." or lower_right == ".":
            return False
        
        return True

    def water_around_boat1(self, row: int, col: int):

        if board.is_upper_left(row, col):
            self.grid[row+1][col] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row+1][col+1] = "w"

        elif board.is_upper_right(row, col):
            self.grid[row+1][col] = "w"
            self.grid[row][col-1] = "w"
            self.grid[row+1][col-1] = "w"

        elif board.is_lower_left(row, col):
            self.grid[row-1][col] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row-1][col+1] = "w"

        elif board.is_lower_right(row, col):
            self.grid[row-1][col] = "w"
            self.grid[row][col-1] = "w"
            self.grid[row-1][col-1] = "w"

        elif self.is_upper_middle(row,col):
            self.grid[row][col-1] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row+1][col-1] = "w"
            self.grid[row+1][col] = "w"
            self.grid[row+1][col+1] = "w"

        elif self.is_lower_middle(row,col):
            self.grid[row][col-1] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row-1][col-1] = "w"
            self.grid[row-1][col] = "w"
            self.grid[row-1][col+1] = "w"

        elif self.is_left_middle(row,col):
            self.grid[row-1][col] = "w"
            self.grid[row+1][col] = "w"
            self.grid[row-1][col+1] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row+1][col+1] = "w"

        elif self.is_right_middle(row,col):
            self.grid[row-1][col] = "w"
            self.grid[row+1][col] = "w"
            self.grid[row-1][col-1] = "w"
            self.grid[row][col-1] = "w"
            self.grid[row+1][col-1] = "w"

        else:
            self.grid[row-1][col-1] = "w"
            self.grid[row-1][col] = "w"
            self.grid[row-1][col+1] = "w"
            self.grid[row][col-1] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row+1][col-1] = "w"
            self.grid[row+1][col] = "w"
            self.grid[row+1][col+1] = "w"


    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board. """

        from sys import stdin
        
        ROW = stdin.readline().split()      #lè a 1ª linha do ficheiro
        COL = stdin.readline().split()      #lè a 2ª linha do ficheiro

        ROW_counts = [int(ship_count) for ship_count in ROW[1:]]    #lè ROW desde o 2º elemento até ao último na forma int
        COL_counts = [int(ship_count) for ship_count in COL[1:]]

        grid = [['.' for _ in range(10)] for _ in range(10)]   #cria uma matriz 10x10 vazia

        Nhints = int(stdin.readline())

        for _ in range(Nhints):
            hint_line = stdin.readline().split()
            row = int(hint_line[1])
            col = int(hint_line[2])
            ship_type = hint_line[3]
            grid[row][col] = ship_type

        return Board(grid, ROW_counts, COL_counts)

    def w(self, row: int, col: int):
        self.grid[row][col] = "w"

    def c(self, row: int, col: int):
        self.grid[row][col] = "c"

    def t(self, row: int, col: int):
        self.grid[row][col] = "t"

    def m(self, row: int, col: int):
        self.grid[row][col] = "m"

    def b(self, row: int, col: int):
        self.grid[row][col] = "b"

    def l(self, row: int, col: int):
        self.grid[row][col] = "l"

    def r(self, row: int, col: int):
        self.grid[row][col] = "r"

    def print(self):
        for row in self.grid:
            print(" ".join(row))







class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        result = []    #lista de ações
        board = state.board

        # Meter água se ROW_counts estiver a 0

        for row in range(10):
            if board.ROW_counts[row] == 0:
                result.append((row, "Put water in row"))

        # Meter água se COL_counts estiver a 0

        for col in range(10):
            if board.COL_counts[col] == 0:
                result.append((col, "Put water in column"))
        
        # Meter água à volta dos boat1

        for row in range(10):
            for col in range(10):
                if better_lower(board.get_value(row, col)) == "c":
                    if not board.is_water_around_boat1(row, col):
                        result.append((row, col, "Water around boat1"))

        
                        
        # Meter barcos se o nº de células vazias for igual a ROW_counts
        """
        for row in range(10):
            dot_counter = 0
            for col in range(10):
                if board.get_value(row, col) == '.':    # só verifica as contagens se ainda houver células vazias
                    dot_counter += 1
            
            if board.ROW_counts[row] == dot_counter:    # nº de "." igual à contagem da ROW
                for col in range(10):
                    if board.get_value(row, col) == ".":
                        left, right = board.adjacent_horizontal_values(row, col)
                        above, below = board.adjacent_vertical_values(row, col)
                        left = left.lower()
                        right = right.lower()
                        above = above.lower()
                        below = below.lower()

                        if left == "w" and right == "w" and above == "w" and below == "w":
                            board.grid[row][col] = "c"

                        #if board.ROW_counts[row] >= 4:
                            """


        # Meter barcos se o nº de células vazias for igual a COL_counts
        """
        for col in range(10):
            dot_counter = 0
            for row in range(10):
                if board.get_value(row, col) == '.':    # só verifica as contagens se ainda houver células vazias
                    dot_counter += 1
            
            if board.COL_counts[col] == dot_counter:    # nº de "." igual à contagem da ROW
                for row in range(10):
                    if board.get_value(row, col) == ".":
                        board.grid[row][col] = "s"      # navio não identificado ainda
        """
        # Atualizar barcos não identificados "s"
        
        return result

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        board = state.board
        grid_copy = state.board.grid.copy()
        ROW_counts_copy = board.ROW_counts.copy()
        COL_counts_copy = board.COL_counts.copy()
        n_action_args = len(action)

        if n_action_args == 2:
            first, second = action
            if second == "Put water in row":
                row = first
                for col in range(10):
                    if board.get_value(row, col) == '.':
                        board.grid[row][col] = "w"

            elif second == "Put water in column":
                col = first
                for row in range(10):
                    if board.get_value(row, col) == '.':
                        board.grid[row][col] = "w"


        elif n_action_args == 3:

            row, col, third = action

            if third == "Water around boat1":

                board.water_around_boat1(row, col)

            """grid_copy[row][col] = ship_type

            if ship_type != 'w':                #ROW_counts e COL_counts é o nº de navios que faltam colocar na linha/coluna
                ROW_counts_copy[row] -= 1
                COL_counts_copy[col] -= 1"""

        new_board = Board(grid_copy, ROW_counts_copy, COL_counts_copy)
        new_state = BimaruState(new_board)

        new_board.print()
        print("\n")

        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        for row in state.board.grid:
            for cell in row:
                if cell == ".":
                    return False     # se encontrar pelo menos 1 célula vazia, então ainda não acabou
        
        # No fim as águas são substituídas por células vazias para melhor visualização da grelha

        for row in range(10):
            for col in range(10):
                if board.get_value[row][col].lower() == "w":
                    board.grid[row][col] = "."

        return True

    def h(self, node: Node):    #nº de navios que falta serem colocados (é admissível)
        """Função heuristica utilizada para a procura A*."""
        
        state = node.state
        count = sum(state.board.ROW_counts) + sum(state.board.COL_counts)

        return count

if __name__ == "__main__":

    board = Board.parse_instance()

    # Criar uma instância de Bimaru:
    problem = Bimaru(board)

    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.print(), sep="")