# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 162:
# 96556 Miguel Moreira
# 95657 Pedro Almeida

import sys
from sys import stdout
import numpy as np
import copy
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

    def __init__(self, grid, ROW_counts, COL_counts, remaining_boats):
        self.grid = grid
        self.ROW_counts = ROW_counts
        self.COL_counts = COL_counts
        self.remaining_boats = remaining_boats

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        
        return self.grid[row][col]
    
    def water_row_column(self, row: int, col: int):

        dot_counter = 0
        for j in range(10):
            if self.grid[row][j] == ".":
                dot_counter += 1

        if self.ROW_counts[row] == 0 and dot_counter != 0:
            for j in range(10):
                if self.grid[row][j] == ".":
                    self.grid[row][j] = "w"

        dot_counter = 0
        for i in range(10):
            if self.grid[i][col] == ".":
                dot_counter += 1

        if self.COL_counts[col] == 0 and dot_counter != 0:
            for i in range(10):
                if self.grid[i][col] == ".":
                    self.grid[i][col] = "w"

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

        if left == "." or right == "." or above == "." or below == "." or upper_left == "." or upper_right == "." or lower_left == "." or lower_right == ".":
            return False
        
        return True

    def is_valid(self, value):

        return value == None or better_lower(value) == "." or better_lower(value) == "w"

    def is_valid_boat4_place(self, row: int, col: int, beginning):
        
        if better_lower(beginning) == "t":
            # check if sides are valid
            left, right = self.adjacent_horizontal_values(row+1, col)
            if self.is_valid(left) and self.is_valid(right):
                left, right = self.adjacent_horizontal_values(row+2, col)
                if self.is_valid(left) and self.is_valid(right):
                    left, right = self.adjacent_horizontal_values(row+3, col)
                    if self.is_valid(left) and self.is_valid(right):
                        # check if extremities are ok
                        above, below = self.adjacent_vertical_values(row, col)
                        upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col)
                        if self.is_valid(above) and self.is_valid(upper_left) and self.is_valid(upper_right):
                            above, below = self.adjacent_vertical_values(row+3, col)
                            upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row+3, col)
                            if self.is_valid(below) and self.is_valid(lower_left) and self.is_valid(lower_right):
                                return True
                                
        elif better_lower(beginning) == "l":
            # check if sides are valid
            above, below = self.adjacent_vertical_values(row, col+1)
            if self.is_valid(above) and self.is_valid(below):
                above, below = self.adjacent_vertical_values(row, col+2)
                if self.is_valid(above) and self.is_valid(below):
                    above, below = self.adjacent_vertical_values(row, col+3)
                    if self.is_valid(above) and self.is_valid(below):
                        # check if extremities are ok
                        left, right = self.adjacent_horizontal_values(row, col)
                        upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col)
                        if self.is_valid(left) and self.is_valid(upper_left) and self.is_valid(lower_left):
                            left, right = self.adjacent_horizontal_values(row, col+3)
                            upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col+3)
                            if self.is_valid(right) and self.is_valid(upper_right) and self.is_valid(lower_right):
                                return True
                
        return False

    def is_valid_boat3_place(self, row: int, col: int, beginning):
        
        if better_lower(beginning) == "t":
            # check if sides are valid
            left, right = self.adjacent_horizontal_values(row+1, col)
            if self.is_valid(left) and self.is_valid(right):
                left, right = self.adjacent_horizontal_values(row+2, col)
                if self.is_valid(left) and self.is_valid(right):
                    # check if extremities are ok
                    above, below = self.adjacent_vertical_values(row, col)
                    upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col)
                    if self.is_valid(above) and self.is_valid(upper_left) and self.is_valid(upper_right):
                        above, below = self.adjacent_vertical_values(row+2, col)
                        upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row+2, col)
                        if self.is_valid(below) and self.is_valid(lower_left) and self.is_valid(lower_right):
                            return True
                                
        elif better_lower(beginning) == "l":
            # check if sides are valid
            above, below = self.adjacent_vertical_values(row, col+1)
            if self.is_valid(above) and self.is_valid(below):
                above, below = self.adjacent_vertical_values(row, col+2)
                if self.is_valid(above) and self.is_valid(below):
                    # check if extremities are ok
                    left, right = self.adjacent_horizontal_values(row, col)
                    upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col)
                    if self.is_valid(left) and self.is_valid(upper_left) and self.is_valid(lower_left):
                        left, right = self.adjacent_horizontal_values(row, col+2)
                        upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col+2)
                        if self.is_valid(right) and self.is_valid(upper_right) and self.is_valid(lower_right):
                            return True
                
        return False

    def is_valid_boat2_place(self, row: int, col: int, beginning):
        
        if better_lower(beginning) == "t":
            # check if sides are valid
            left, right = self.adjacent_horizontal_values(row+1, col)
            if self.is_valid(left) and self.is_valid(right):
                # check if extremities are ok
                above, below = self.adjacent_vertical_values(row, col)
                upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col)
                if self.is_valid(above) and self.is_valid(upper_left) and self.is_valid(upper_right):
                    above, below = self.adjacent_vertical_values(row+1, col)
                    upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row+1, col)
                    if self.is_valid(below) and self.is_valid(lower_left) and self.is_valid(lower_right):
                        return True
                                
        elif better_lower(beginning) == "l":
            # check if sides are valid
            above, below = self.adjacent_vertical_values(row, col+1)
            if self.is_valid(above) and self.is_valid(below):
                # check if extremities are ok
                left, right = self.adjacent_horizontal_values(row, col)
                upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col)
                if self.is_valid(left) and self.is_valid(upper_left) and self.is_valid(lower_left):
                    left, right = self.adjacent_horizontal_values(row, col+1)
                    upper_left, upper_right, lower_left, lower_right = self.adjacent_diagonal_values(row, col+1)
                    if self.is_valid(right) and self.is_valid(upper_right) and self.is_valid(lower_right):
                        return True
                
        return False

    def water_adjacent_vertical(self, row: int, col: int):

        if row == 0:
            if self.get_value(row+1, col) == ".":
                self.grid[row+1][col] = "w"

        elif row == 9:
            if self.get_value(row-1, col) == ".":
                self.grid[row-1][col] = "w"

        else:
            if self.get_value(row-1, col) == ".":
                self.grid[row-1][col] = "w"
            if self.get_value(row+1, col) == ".":
                self.grid[row+1][col] = "w"

    def water_adjacent_horizontal(self, row: int, col: int):

        if col == 0:
            if self.get_value(row, col+1) == ".":
                self.grid[row][col+1] = "w"

        elif col == 9:
            if self.get_value(row, col-1) == ".":
                self.grid[row][col-1] = "w"

        else:
            if self.get_value(row, col-1) == ".":
                self.grid[row][col-1] = "w"
            if self.get_value(row, col+1) == ".":
                self.grid[row][col+1] = "w"

    def water_adjacent_diagonal(self, row: int, col: int):

        if self.is_upper_left(row, col):
            if self.grid[row+1][col+1] == ".":
                self.grid[row+1][col+1] = "w"
        
        elif self.is_upper_right(row, col):
            if self.grid[row+1][col-1] == ".":
                self.grid[row+1][col-1] = "w"
        
        elif self.is_lower_left(row, col):
            if self.grid[row-1][col+1] == ".":
                self.grid[row-1][col+1] = "w"
        
        elif self.is_lower_right(row, col):
            if self.grid[row-1][col-1] == ".":
                self.grid[row-1][col-1] = "w"
        
        elif self.is_upper_middle(row, col):
            if self.grid[row+1][col-1] == ".":
                self.grid[row+1][col-1] = "w"
            if self.grid[row+1][col+1] == ".":
                self.grid[row+1][col+1] = "w"
        
        elif self.is_lower_middle(row, col):
            if self.grid[row-1][col-1] == ".":
                self.grid[row-1][col-1] = "w"
            if self.grid[row-1][col+1] == ".":
                self.grid[row-1][col+1] = "w"
        
        elif self.is_left_middle(row, col):
            if self.grid[row-1][col+1] == ".":
                self.grid[row-1][col+1] = "w"
            if self.grid[row+1][col+1] == ".":
                self.grid[row+1][col+1] = "w"
        
        elif self.is_right_middle(row, col):
            if self.grid[row-1][col-1] == ".":
                self.grid[row-1][col-1] = "w"
            if self.grid[row+1][col-1] == ".":
                self.grid[row+1][col-1] = "w"
        
        else:
            if self.grid[row-1][col-1] == ".":
                self.grid[row-1][col-1] = "w"
            if self.grid[row-1][col+1] == ".":
                self.grid[row-1][col+1] = "w"
            if self.grid[row+1][col-1] == ".":
                self.grid[row+1][col-1] = "w"
            if self.grid[row+1][col+1] == ".":
                self.grid[row+1][col+1] = "w"

    def water_around_boat1(self, row: int, col: int):

        self.water_adjacent_horizontal(row, col)
        self.water_adjacent_vertical(row, col)
        self.water_adjacent_diagonal(row, col)

        """if self.is_upper_left(row, col):
            self.grid[row+1][col] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row+1][col+1] = "w"

        elif self.is_upper_right(row, col):
            self.grid[row+1][col] = "w"
            self.grid[row][col-1] = "w"
            self.grid[row+1][col-1] = "w"

        elif self.is_lower_left(row, col):
            self.grid[row-1][col] = "w"
            self.grid[row][col+1] = "w"
            self.grid[row-1][col+1] = "w"

        elif self.is_lower_right(row, col):
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
            self.grid[row+1][col+1] = "w"""

    def water_around_boat2(self, row: int, col: int, beginning):

        if beginning == "t":
            self.water_adjacent_horizontal(row, col)
            self.water_adjacent_horizontal(row+1, col)
            self.water_adjacent_diagonal(row, col)      # as extremidades
            self.water_adjacent_vertical(row, col)
            self.water_adjacent_diagonal(row+1, col)
            self.water_adjacent_vertical(row+1, col)

        elif beginning == "l":
            self.water_adjacent_horizontal(row, col)
            self.water_adjacent_horizontal(row, col+1)
            self.water_adjacent_diagonal(row, col)      # as extremidades
            self.water_adjacent_vertical(row, col)
            self.water_adjacent_diagonal(row, col+1)
            self.water_adjacent_vertical(row, col+1)

    def water_around_boat3(self, row: int, col: int, beginning):

        if beginning == "t":
            self.water_adjacent_horizontal(row, col)
            self.water_adjacent_horizontal(row+1, col)
            self.water_adjacent_horizontal(row+2, col)
            self.water_adjacent_diagonal(row, col)      # as extremidades
            self.water_adjacent_vertical(row, col)
            self.water_adjacent_diagonal(row+2, col)
            self.water_adjacent_vertical(row+2, col)

        elif beginning == "l":
            self.water_adjacent_horizontal(row, col)
            self.water_adjacent_horizontal(row, col+1)
            self.water_adjacent_horizontal(row, col+2)
            self.water_adjacent_diagonal(row, col)      # as extremidades
            self.water_adjacent_vertical(row, col)
            self.water_adjacent_diagonal(row, col+2)
            self.water_adjacent_vertical(row, col+2)

    def water_around_boat4(self, row: int, col: int, beginning):

        if beginning == "t":
            self.water_adjacent_horizontal(row, col)
            self.water_adjacent_horizontal(row+1, col)
            self.water_adjacent_horizontal(row+2, col)
            self.water_adjacent_horizontal(row+3, col)
            self.water_adjacent_diagonal(row, col)      # as extremidades
            self.water_adjacent_vertical(row, col)
            self.water_adjacent_diagonal(row+3, col)
            self.water_adjacent_vertical(row+3, col)

        elif beginning == "l":
            self.water_adjacent_horizontal(row, col)
            self.water_adjacent_horizontal(row, col+1)
            self.water_adjacent_horizontal(row, col+2)
            self.water_adjacent_horizontal(row, col+3)
            self.water_adjacent_diagonal(row, col)      # as extremidades
            self.water_adjacent_vertical(row, col)
            self.water_adjacent_diagonal(row, col+3)
            self.water_adjacent_vertical(row, col+3)


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
            if ship_type != "W":
                ROW_counts[row] -= 1
                COL_counts[col] -= 1
        
        # Nº de boat1 já postos

        boat1_counter = 0
        for row in range(10):
            for col in range(10):
                if grid[row][col] == "C":
                    boat1_counter += 1

        # Nº de boat2 já postos

        boat2_counter = 0
        for row in range(10):
            for col in range(10):
                if (grid[row][col] == "T" and grid[row+1][col] == "B") or (grid[row][col] == "L" and grid[row][col+1] == "R"):
                    boat2_counter += 1

        # Nº de boat3 já postos

        boat3_counter = 0
        for row in range(10):
            for col in range(10):
                if (grid[row][col] == "T" and grid[row+1][col] == "M" and grid[row+2][col] == "B") or (grid[row][col] == "L" and grid[row][col+1] == "M" and grid[row][col+2] == "R"):
                    boat3_counter += 1

        # Nº de boat4 já postos

        boat4_counter = 0
        for row in range(10):
            for col in range(10):
                if (grid[row][col] == "T" and grid[row+1][col] == "M" and grid[row+2][col] == "M" and grid[row+3][col] == "B") or (grid[row][col] == "L" and grid[row][col+1] == "M" and grid[row][col+2] == "M" and grid[row][col+3] == "R"):
                    boat4_counter += 1


        remaining_boats = []
        remaining_boats.append(1-boat4_counter)        # Boat4
        remaining_boats.append(2-boat3_counter)        # Boat3
        remaining_boats.append(3-boat2_counter)        # Boat2
        remaining_boats.append(4-boat1_counter)        # Boat1
        board = Board(grid, ROW_counts, COL_counts, remaining_boats)

        # Meter água nas linhas e colunas onde faz sentido

        for row in range(10):
            for col in range(10):
                board.water_row_column(row, col)

        # Meter água à volta dos boat1

        for row in range(10):
            for col in range(10):
                if better_lower(board.get_value(row, col)) == "c":
                    if not board.is_water_around_boat1(row, col):
                        board.water_around_boat1(row, col)

        #board.print2()
        #print("\n")
        return board

    def print2(self):
        for row in range(10):
            for col in range(10):
                stdout.write(self.grid[row][col])
                #stdout.write(" ")
            stdout.write("\n")






class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        result = []    #lista de ações

        # Mete primeiro os boat4

        if state.board.remaining_boats[0] > 0:

            # Meter boat4 vertical

            for col in range(10):
                if state.board.COL_counts[col] >= 3:        # meter barco se já lá estiver um top, middle ou bottom
                    for row in range(10):
                        if better_lower(state.board.get_value(row, col)) == "t":
                            if row <= 6:
                                if state.board.ROW_counts[row+1] != 0 and state.board.ROW_counts[row+2] != 0 and state.board.ROW_counts[row+3] != 0:
                                    # check if there is space
                                    if state.board.get_value(row+1, col) == "." and state.board.get_value(row+2, col) == "." and state.board.get_value(row+3, col) == ".":
                                        if state.board.is_valid_boat4_place(row, col, "t"):
                                            result.append((row, col, "down", "t", "Place boat4"))
                                                    

                        if better_lower(state.board.get_value(row, col)) == "b":
                            if row >= 3:
                                if state.board.ROW_counts[row-1] != 0 and state.board.ROW_counts[row-2] != 0 and state.board.ROW_counts[row-3] != 0:
                                    # check if there is space
                                    if state.board.get_value(row-1, col) == "." and state.board.get_value(row-2, col) == "." and state.board.get_value(row-3, col) == ".":
                                        if state.board.is_valid_boat4_place(row-3, col, "t"):
                                            result.append((row, col, "up", "b", "Place boat4"))
                                                    

                        if better_lower(state.board.get_value(row, col)) == "m":
                            if row != 0 and row != 9:
                                if row == 1:
                                    if state.board.ROW_counts[row-1] != 0 and state.board.ROW_counts[row+1] != 0 and state.board.ROW_counts[row+2] != 0:
                                        # check if there is space
                                        if state.board.get_value(row-1, col) == "." and state.board.get_value(row+1, col) == "." and state.board.get_value(row+2, col) == ".":
                                            if state.board.is_valid_boat4_place(row-1, col, "t"):
                                                result.append((row, col, "down", "m", "Place boat4"))
                                                        

                                elif row == 8:
                                    if state.board.ROW_counts[row-2] != 0 and state.board.ROW_counts[row-1] != 0 and state.board.ROW_counts[row+1] != 0:
                                        # check if there is space
                                        if state.board.get_value(row-2, col) == "." and state.board.get_value(row-1, col) == "." and state.board.get_value(row+1, col) == ".":
                                            if state.board.is_valid_boat4_place(row-2, col, "t"):
                                                result.append((row, col, "up", "m", "Place boat4"))
                                                        

                                else:
                                    if state.board.ROW_counts[row-1] != 0 and state.board.ROW_counts[row+1] != 0:
                                        if state.board.ROW_counts[row+2] != 0:
                                            # check if there is space
                                            if state.board.get_value(row-1, col) == "." and state.board.get_value(row+1, col) == "." and state.board.get_value(row+2, col) == ".":
                                                if state.board.is_valid_boat4_place(row-1, col, "t"):
                                                    result.append((row, col, "down", "m", "Place boat4"))
                                                                

                                        if state.board.ROW_counts[row-2] != 0:
                                            # check if there is space
                                            if state.board.get_value(row-2, col) == "." and state.board.get_value(row-1, col) == "." and state.board.get_value(row+1, col) == ".":
                                                if state.board.is_valid_boat4_place(row-2, col, "t"):
                                                    result.append((row, col, "up", "m", "Place boat4"))
                                                                

            # Meter boat4 horizontal

            for row in range(10):
                if state.board.ROW_counts[row] >= 3:        # meter barco se já lá estiver um left, middle ou right
                    for col in range(10):
                        if better_lower(state.board.get_value(row, col)) == "l":
                            if col <= 6:
                                if state.board.COL_counts[col+1] != 0 and state.board.COL_counts[col+2] != 0 and state.board.COL_counts[col+3] != 0:
                                    # check if there is space
                                    if state.board.get_value(row, col+1) == "." and state.board.get_value(row, col+2) == "." and state.board.get_value(row, col+3) == ".":
                                        if state.board.is_valid_boat4_place(row, col, "l"):
                                            result.append((row, col, "right", "l", "Place boat4"))
                                                    

                        if better_lower(state.board.get_value(row, col)) == "r":
                            if col >= 3:
                                if state.board.COL_counts[col-1] != 0 and state.board.COL_counts[col-2] != 0 and state.board.COL_counts[col-3] != 0:
                                    # check if there is space
                                    if state.board.get_value(row, col-1) == "." and state.board.get_value(row, col-2) == "." and state.board.get_value(row, col-3) == ".":
                                        if state.board.is_valid_boat4_place(row, col-3, "l"):
                                            result.append((row, col, "left", "r", "Place boat4"))
                                                    
                
                        if better_lower(state.board.get_value(row, col)) == "m":
                            if col != 0 and col != 9:
                                if col == 1:
                                    if state.board.COL_counts[col-1] != 0 and state.board.COL_counts[col+1] != 0 and state.board.COL_counts[col+2] != 0:
                                        # check if there is space
                                        if state.board.get_value(row, col-1) == "." and state.board.get_value(row, col+1) == "." and state.board.get_value(row, col+2) == ".":
                                            if state.board.is_valid_boat4_place(row, col-1, "l"):
                                                result.append((row, col, "right", "m", "Place boat4"))
                                                    

                                if col == 8:
                                    if state.board.COL_counts[col-2] != 0 and state.board.COL_counts[col-1] != 0 and state.board.COL_counts[col+1] != 0:
                                        # check if there is space
                                        if state.board.get_value(row, col-2) == "." and state.board.get_value(row, col-1) == "." and state.board.get_value(row, col+1) == ".":
                                            if state.board.is_valid_boat4_place(row, col-2, "l"):
                                                result.append((row, col, "left", "m", "Place boat4"))
                                                    

                                else:
                                    if state.board.COL_counts[col-1] != 0 and state.board.COL_counts[col+1] != 0:
                                        if state.board.COL_counts[col+2] != 0:
                                            # check if there is space
                                            if state.board.get_value(row, col-1) == "." and state.board.get_value(row, col+1) == "." and state.board.get_value(row, col+2) == ".":
                                                if state.board.is_valid_boat4_place(row, col-1, "l"):
                                                    result.append((row, col, "right", "m", "Place boat4"))
                                                            

                                        if state.board.COL_counts[col-2] != 0:
                                            # check if there is space
                                            if state.board.get_value(row, col-2) == "." and state.board.get_value(row, col-1) == "." and state.board.get_value(row, col+1) == ".":
                                                if state.board.is_valid_boat4_place(row, col-2, "l"):
                                                    result.append((row, col, "left", "m", "Place boat4"))
                                                            
            # Meter boat4 vertical

            for col in range(10):
                if state.board.COL_counts[col] >= 4:        # meter barco se houver 4 espaços seguidos
                    for row in range(10):
                        if row <= 6:
                            if state.board.ROW_counts[row] != 0 and state.board.ROW_counts[row+1] != 0 and state.board.ROW_counts[row+2] != 0 and state.board.ROW_counts[row+3] != 0:
                                # check if there is space
                                if state.board.get_value(row, col) == "." and state.board.get_value(row+1, col) == "." and state.board.get_value(row+2, col) == "." and state.board.get_value(row+3, col) == ".":
                                    left, right = state.board.adjacent_horizontal_values(row, col)
                                    if state.board.is_valid(left) and state.board.is_valid(right):
                                        if state.board.is_valid_boat4_place(row, col, "t"):
                                            result.append((row, col, "down", ".", "Place boat4"))
                                                    
            # Meter boat4 horizontal

            for row in range(10):
                if state.board.ROW_counts[row] >= 4:        # meter barco se houver 4 espaços seguidos
                    for col in range(10):
                        if col <= 6:
                            if state.board.COL_counts[col] != 0 and state.board.COL_counts[col+1] != 0 and state.board.COL_counts[col+2] != 0 and state.board.COL_counts[col+3] != 0:
                                # check if there is space
                                if state.board.get_value(row, col) == "." and state.board.get_value(row, col+1) == "." and state.board.get_value(row, col+2) == "." and state.board.get_value(row, col+3) == ".":
                                    above, below = state.board.adjacent_vertical_values(row, col)
                                    if state.board.is_valid(above) and state.board.is_valid(below):
                                        if state.board.is_valid_boat4_place(row, col, "l"):
                                            result.append((row, col, "right", ".", "Place boat4"))

            # Se o boat4 estiver posto, mete os boat3

        else:
            if state.board.remaining_boats[1] > 0:

                # Meter boat3 vertical
                
                for col in range(10):
                    if state.board.COL_counts[col] >= 2:        # meter barco se já lá estiver um top, middle ou bottom
                        for row in range(10):
                            if better_lower(state.board.get_value(row, col)) == "t":
                                if row <= 7:
                                    if state.board.ROW_counts[row+1] != 0 and state.board.ROW_counts[row+2] != 0:
                                        # check if there is space
                                        if state.board.get_value(row+1, col) == "." and state.board.get_value(row+2, col) == ".":
                                            if state.board.is_valid_boat3_place(row, col, "t"):
                                                result.append((row, col, "down", "t", "Place boat3"))
                                                    

                            if better_lower(state.board.get_value(row, col)) == "b":
                                if row >= 2:
                                    if state.board.ROW_counts[row-1] != 0 and state.board.ROW_counts[row-2] != 0:
                                        # check if there is space
                                        if state.board.get_value(row-1, col) == "." and state.board.get_value(row-2, col) == ".":
                                            if state.board.is_valid_boat3_place(row-2, col, "t"):
                                                result.append((row, col, "up", "b", "Place boat3"))
                                                    

                            if better_lower(state.board.get_value(row, col)) == "m":
                                if row != 0 and row != 9:
                                    if state.board.ROW_counts[row-1] != 0 and state.board.ROW_counts[row+1] != 0:
                                        # check if there is space
                                        if state.board.get_value(row-1, col) == "." and state.board.get_value(row+1, col) == ".":
                                            if state.board.is_valid_boat3_place(row-1, col, "t"):
                                                result.append((row, col, "vertical", "m", "Place boat3"))
                                                    

                # Meter boat3 horizontal

                for row in range(10):
                    if state.board.ROW_counts[row] >= 2:        # meter barco se já lá estiver um left, middle ou right
                        for col in range(10):
                            if better_lower(state.board.get_value(row, col)) == "l":
                                if col <= 7:
                                    if state.board.COL_counts[col+1] != 0 and state.board.COL_counts[col+2] != 0:
                                        # check if there is space
                                        if state.board.get_value(row, col+1) == "." and state.board.get_value(row, col+2) == ".":
                                            if state.board.is_valid_boat3_place(row, col, "l"):
                                                result.append((row, col, "right", "l", "Place boat3"))
                                                    

                            if better_lower(state.board.get_value(row, col)) == "r":
                                if col >= 2:
                                    if state.board.COL_counts[col-1] != 0 and state.board.COL_counts[col-2] != 0:
                                        # check if there is space
                                        if state.board.get_value(row, col-1) == "." and state.board.get_value(row, col-2) == ".":
                                            if state.board.is_valid_boat3_place(row, col-2, "l"):
                                                result.append((row, col, "left", "r", "Place boat3"))
                                                    

                            if better_lower(state.board.get_value(row, col)) == "m":
                                if col != 0 and col != 9:
                                    if state.board.COL_counts[col-1] != 0 and state.board.COL_counts[col+1] != 0:
                                        # check if there is space
                                        if state.board.get_value(row, col-1) == "." and state.board.get_value(row, col+1) == ".":
                                            if state.board.is_valid_boat3_place(row, col-1, "l"):
                                                result.append((row, col, "horizontal", "m", "Place boat3"))

                                
                # Meter boat3 vertical

                for col in range(10):
                    if state.board.COL_counts[col] >= 3:        # meter barco se houver 3 espaços seguidos
                        for row in range(10):
                            if row <= 7:
                                if state.board.ROW_counts[row] != 0 and state.board.ROW_counts[row+1] != 0 and state.board.ROW_counts[row+2] != 0:
                                    # check if there is space
                                    if state.board.get_value(row, col) == "." and state.board.get_value(row+1, col) == "." and state.board.get_value(row+2, col) == ".":
                                        left, right = state.board.adjacent_horizontal_values(row, col)
                                        if state.board.is_valid(left) and state.board.is_valid(right):
                                            if state.board.is_valid_boat3_place(row, col, "t"):
                                                result.append((row, col, "down", ".", "Place boat3"))
                                                                
                                                            
                # Meter boat3 horizontal

                for row in range(10):
                    if state.board.ROW_counts[row] >= 3:        # meter barco se houver 3 espaços seguidos
                        for col in range(10):
                            if col <= 7:
                                if state.board.COL_counts[col] != 0 and state.board.COL_counts[col+1] != 0 and state.board.COL_counts[col+2] != 0:
                                    # check if there is space
                                    if state.board.get_value(row, col) == "." and state.board.get_value(row, col+1) == "." and state.board.get_value(row, col+2) == ".":
                                        above, below = state.board.adjacent_vertical_values(row, col)
                                        if state.board.is_valid(above) and state.board.is_valid(below):
                                            if state.board.is_valid_boat3_place(row, col, "l"):
                                                result.append((row, col, "right", ".", "Place boat3"))          

                # Se os boat3 estiverem postos, mete os boat2

            else:
                if state.board.remaining_boats[2] > 0:

                    # Meter boat2 vertical

                    for col in range(10):
                        if state.board.COL_counts[col] >= 1:        # meter barco se já lá estiver um top ou bottom
                            for row in range(10):
                                if better_lower(state.board.get_value(row, col)) == "t":
                                    if row <= 8:
                                        if state.board.ROW_counts[row+1] != 0:
                                            # check if there is space
                                            if state.board.get_value(row+1, col) == ".":
                                                if state.board.is_valid_boat2_place(row, col, "t"):
                                                    result.append((row, col, "down", "t", "Place boat2"))
                                                    
                                                
                                if better_lower(state.board.get_value(row, col)) == "b":
                                    if row >= 1:
                                        if state.board.ROW_counts[row-1] != 0:
                                            # check if there is space
                                            if state.board.get_value(row-1, col) == ".":
                                                if state.board.is_valid_boat2_place(row-1, col, "t"):
                                                    result.append((row, col, "up", "b", "Place boat2"))
                                                    

                    # Meter boat2 horizontal
                    for row in range(10):
                        if state.board.ROW_counts[row] >= 1:        # meter barco se já lá estiver um left ou right
                            for col in range(10):
                                if better_lower(state.board.get_value(row, col)) == "l":
                                    if col <= 8:
                                        if state.board.COL_counts[col+1] != 0:
                                            # check if there is space
                                            if state.board.get_value(row, col+1) == ".":
                                                if state.board.is_valid_boat2_place(row, col, "l"):
                                                    result.append((row, col, "right", "l", "Place boat2"))
                                                    
                                                
                                if better_lower(state.board.get_value(row, col)) == "r":
                                    if col >= 1:
                                        if state.board.COL_counts[col-1] != 0:
                                            # check if there is space
                                            if state.board.get_value(row, col-1) == ".":
                                                if state.board.is_valid_boat2_place(row, col-1, "l"):
                                                    result.append((row, col, "left", "r", "Place boat2"))
                                                
                    # Meter boat2 vertical

                    for col in range(10):
                        if state.board.COL_counts[col] >= 2:        # meter barco se houver 2 espaços seguidos
                            for row in range(10):
                                if row <= 8:
                                    if state.board.ROW_counts[row] != 0 and state.board.ROW_counts[row+1] != 0:
                                        # check if there is space
                                        if state.board.get_value(row, col) == "." and state.board.get_value(row+1, col) == ".":
                                            left, right = state.board.adjacent_horizontal_values(row, col)
                                            if state.board.is_valid(left) and state.board.is_valid(right):
                                                if state.board.is_valid_boat2_place(row, col, "t"):
                                                    result.append((row, col, "down", ".", "Place boat2"))
                                                    

                    # Meter boat2 horizontal

                    for row in range(10):
                        if state.board.ROW_counts[row] >= 2:        # meter barco se houver 2 espaços seguidos
                            for col in range(10):
                                if col <= 8:
                                    if state.board.COL_counts[col] != 0 and state.board.COL_counts[col+1] != 0:
                                        # check if there is space
                                        if state.board.get_value(row, col) == "." and state.board.get_value(row, col+1) == ".":
                                            above, below = state.board.adjacent_vertical_values(row, col)
                                            if state.board.is_valid(above) and state.board.is_valid(below):
                                                if state.board.is_valid_boat2_place(row, col, "l"):
                                                    result.append((row, col, "right", ".", "Place boat2"))

                    # Se os boat2 estiverem postos, mete os boat1

                else:
                    if state.board.remaining_boats[3] > 0:
                        for row in range(10):
                            if state.board.ROW_counts[row] != 0:
                                for col in range(10):
                                    if state.board.COL_counts[col] != 0:
                                        if state.board.get_value(row, col) == ".":
                                            above, below = state.board.adjacent_vertical_values(row, col)
                                            left, right = state.board.adjacent_horizontal_values(row, col)
                                            upper_left, upper_right, lower_left, lower_right = state.board.adjacent_diagonal_values(row, col)
                                            if state.board.is_valid(above) and state.board.is_valid(below) and state.board.is_valid(left) and state.board.is_valid(right) and state.board.is_valid(upper_left) and state.board.is_valid(upper_right) and state.board.is_valid(lower_left) and state.board.is_valid(lower_right):
                                                result.append((row, col, "Place boat1"))


        #print(result)
        return result

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        #new_state = copy.deepcopy(state)
        #grid_copy = state.board.grid.copy()
        #ROW_counts_copy = state.board.ROW_counts.copy()
        #COL_counts_copy = state.board.COL_counts.copy()
        #remaining_boats_copy = state.board.remaining_boats.copy()
        new_board = copy.deepcopy(state.board)

        n_action_args = len(action)

        if n_action_args == 5:
            row, col, orientation, starting_boat, type = action
            if type == "Place boat4":
                if starting_boat == "b":
                    new_board.grid[row-1][col] = "m"
                    new_board.grid[row-2][col] = "m"
                    new_board.grid[row-3][col] = "t"
                    new_board.water_around_boat4(row-3, col, "t")
                    new_board.COL_counts[col] -= 3
                    new_board.ROW_counts[row-1] -= 1
                    new_board.ROW_counts[row-2] -= 1
                    new_board.ROW_counts[row-3] -= 1
                    new_board.water_row_column(row-1, col)
                    new_board.water_row_column(row-2, col)
                    new_board.water_row_column(row-3, col)

                elif starting_boat == "l":
                    new_board.grid[row][col+1] = "m"
                    new_board.grid[row][col+2] = "m"
                    new_board.grid[row][col+3] = "r"
                    new_board.water_around_boat4(row, col, "l")
                    new_board.ROW_counts[row] -= 3
                    new_board.COL_counts[col+1] -= 1
                    new_board.COL_counts[col+2] -= 1
                    new_board.COL_counts[col+3] -= 1
                    new_board.water_row_column(row, col+1)
                    new_board.water_row_column(row, col+2)
                    new_board.water_row_column(row, col+3)

                elif starting_boat == "t":
                    new_board.grid[row+1][col] = "m"
                    new_board.grid[row+2][col] = "m"
                    new_board.grid[row+3][col] = "b"
                    new_board.water_around_boat4(row, col, "t")
                    new_board.COL_counts[col] -= 3
                    new_board.ROW_counts[row+1] -= 1
                    new_board.ROW_counts[row+2] -= 1
                    new_board.ROW_counts[row+3] -= 1
                    new_board.water_row_column(row+1, col)
                    new_board.water_row_column(row+2, col)
                    new_board.water_row_column(row+3, col)

                elif starting_boat == "r":
                    new_board.grid[row][col-1] = "m"
                    new_board.grid[row][col-2] = "m"
                    new_board.grid[row][col-3] = "l"
                    new_board.water_around_boat4(row, col-3, "l")
                    new_board.ROW_counts[row] -= 3
                    new_board.COL_counts[col-1] -= 1
                    new_board.COL_counts[col-2] -= 1
                    new_board.COL_counts[col-3] -= 1
                    new_board.water_row_column(row, col-1)
                    new_board.water_row_column(row, col-2)
                    new_board.water_row_column(row, col-3)

                elif starting_boat == "m":
                    if orientation == "up":
                        new_board.grid[row-2][col] = "t"
                        new_board.grid[row-1][col] = "m"
                        new_board.grid[row+1][col] = "b"
                        new_board.water_around_boat4(row-2, col, "t")
                        new_board.COL_counts[col] -= 3
                        new_board.ROW_counts[row-2] -= 1
                        new_board.ROW_counts[row-1] -= 1
                        new_board.ROW_counts[row+1] -= 1
                        new_board.water_row_column(row-2, col)
                        new_board.water_row_column(row-1, col)
                        new_board.water_row_column(row+1, col)

                    elif orientation == "down":
                        new_board.grid[row-1][col] = "t"
                        new_board.grid[row+1][col] = "m"
                        new_board.grid[row+2][col] = "b"
                        new_board.water_around_boat4(row-1, col, "t")
                        new_board.COL_counts[col] -= 3
                        new_board.ROW_counts[row-1] -= 1
                        new_board.ROW_counts[row+1] -= 1
                        new_board.ROW_counts[row+2] -= 1
                        new_board.water_row_column(row-1, col)
                        new_board.water_row_column(row+1, col)
                        new_board.water_row_column(row+2, col)

                    elif orientation == "right":
                        new_board.grid[row][col-1] = "l"
                        new_board.grid[row][col+1] = "m"
                        new_board.grid[row][col+2] = "r"
                        new_board.water_around_boat4(row, col-1, "l")
                        new_board.ROW_counts[row] -= 3
                        new_board.COL_counts[col-1] -= 1
                        new_board.COL_counts[col+1] -= 1
                        new_board.COL_counts[col+2] -= 1
                        new_board.water_row_column(row, col-1)
                        new_board.water_row_column(row, col+1)
                        new_board.water_row_column(row, col+2)

                    elif orientation == "left":
                        new_board.grid[row][col-2] = "l"
                        new_board.grid[row][col-1] = "m"
                        new_board.grid[row][col+1] = "r"
                        new_board.water_around_boat4(row, col-2, "l")
                        new_board.ROW_counts[row] -= 3
                        new_board.COL_counts[col-2] -= 1
                        new_board.COL_counts[col-1] -= 1
                        new_board.COL_counts[col+1] -= 1
                        new_board.water_row_column(row, col-2)
                        new_board.water_row_column(row, col-1)
                        new_board.water_row_column(row, col+1)

                elif starting_boat == ".":
                    if orientation == "down":
                        new_board.grid[row][col] = "t"
                        new_board.grid[row+1][col] = "m"
                        new_board.grid[row+2][col] = "m"
                        new_board.grid[row+3][col] = "b"
                        new_board.water_around_boat4(row, col, "t")
                        new_board.COL_counts[col] -= 4
                        new_board.ROW_counts[row] -= 1
                        new_board.ROW_counts[row+1] -= 1
                        new_board.ROW_counts[row+2] -= 1
                        new_board.ROW_counts[row+3] -= 1
                        new_board.water_row_column(row, col)
                        new_board.water_row_column(row+1, col)
                        new_board.water_row_column(row+2, col)
                        new_board.water_row_column(row+3, col)

                    elif orientation == "right":
                        new_board.grid[row][col] = "l"
                        new_board.grid[row][col+1] = "m"
                        new_board.grid[row][col+2] = "m"
                        new_board.grid[row][col+3] = "r"
                        new_board.water_around_boat4(row, col, "l")
                        new_board.ROW_counts[row] -= 4
                        new_board.COL_counts[col] -= 1
                        new_board.COL_counts[col+1] -= 1
                        new_board.COL_counts[col+2] -= 1
                        new_board.COL_counts[col+3] -= 1
                        new_board.water_row_column(row, col)
                        new_board.water_row_column(row, col+1)
                        new_board.water_row_column(row, col+2)
                        new_board.water_row_column(row, col+3)

                new_board.remaining_boats[0] -= 1


            elif type == "Place boat3":
                if starting_boat == "b":
                    new_board.grid[row-1][col] = "m"
                    new_board.grid[row-2][col] = "t"
                    new_board.water_around_boat3(row-2, col, "t")
                    new_board.COL_counts[col] -= 2
                    new_board.ROW_counts[row-1] -= 1
                    new_board.ROW_counts[row-2] -= 1
                    new_board.water_row_column(row-1, col)
                    new_board.water_row_column(row-2, col)

                elif starting_boat == "l":
                    new_board.grid[row][col+1] = "m"
                    new_board.grid[row][col+2] = "r"
                    new_board.water_around_boat3(row, col, "l")
                    new_board.ROW_counts[row] -= 2
                    new_board.COL_counts[col+1] -= 1
                    new_board.COL_counts[col+2] -= 1
                    new_board.water_row_column(row, col+1)
                    new_board.water_row_column(row, col+2)

                elif starting_boat == "t":
                    new_board.grid[row+1][col] = "m"
                    new_board.grid[row+2][col] = "b"
                    new_board.water_around_boat3(row, col, "t")
                    new_board.COL_counts[col] -= 2
                    new_board.ROW_counts[row+1] -= 1
                    new_board.ROW_counts[row+2] -= 1
                    new_board.water_row_column(row+1, col)
                    new_board.water_row_column(row+2, col)

                elif starting_boat == "r":
                    new_board.grid[row][col-1] = "m"
                    new_board.grid[row][col-2] = "l"
                    new_board.water_around_boat3(row, col-2, "l")
                    new_board.ROW_counts[row] -= 2
                    new_board.COL_counts[col-1] -= 1
                    new_board.COL_counts[col-2] -= 1
                    new_board.water_row_column(row, col-1)
                    new_board.water_row_column(row, col-2)

                elif starting_boat == "m":
                    if orientation == "vertical":
                        new_board.grid[row-1][col] = "t"
                        new_board.grid[row+1][col] = "b"
                        new_board.water_around_boat3(row-1, col, "t")
                        new_board.COL_counts[col] -= 2
                        new_board.ROW_counts[row-1] -= 1
                        new_board.ROW_counts[row+1] -= 1
                        new_board.water_row_column(row-1, col)
                        new_board.water_row_column(row+1, col)

                    elif orientation == "horizontal":
                        new_board.grid[row][col-1] = "l"
                        new_board.grid[row][col+1] = "r"
                        new_board.water_around_boat3(row, col-1, "l")
                        new_board.ROW_counts[row] -= 2
                        new_board.COL_counts[col-1] -= 1
                        new_board.COL_counts[col+1] -= 1
                        new_board.water_row_column(row, col-1)
                        new_board.water_row_column(row, col+1)

                elif starting_boat == ".":
                    if orientation == "down":
                        new_board.grid[row][col] = "t"
                        new_board.grid[row+1][col] = "m"
                        new_board.grid[row+2][col] = "b"
                        new_board.water_around_boat3(row, col, "t")
                        new_board.COL_counts[col] -= 3
                        new_board.ROW_counts[row] -= 1
                        new_board.ROW_counts[row+1] -= 1
                        new_board.ROW_counts[row+2] -= 1
                        new_board.water_row_column(row, col)
                        new_board.water_row_column(row+1, col)
                        new_board.water_row_column(row+2, col)

                    elif orientation == "right":
                        new_board.grid[row][col] = "l"
                        new_board.grid[row][col+1] = "m"
                        new_board.grid[row][col+2] = "r"
                        new_board.water_around_boat3(row, col, "l")
                        new_board.ROW_counts[row] -= 3
                        new_board.COL_counts[col] -= 1
                        new_board.COL_counts[col+1] -= 1
                        new_board.COL_counts[col+2] -= 1
                        new_board.water_row_column(row, col)
                        new_board.water_row_column(row, col+1)
                        new_board.water_row_column(row, col+2)

                new_board.remaining_boats[1] -= 1
                

            elif type == "Place boat2":
                if starting_boat == "b":
                    new_board.grid[row-1][col] = "t"
                    new_board.water_around_boat2(row-1, col, "t")
                    new_board.COL_counts[col] -= 1
                    new_board.ROW_counts[row-1] -= 1
                    new_board.water_row_column(row-1, col)

                elif starting_boat == "l":
                    new_board.grid[row][col+1] = "r"
                    new_board.water_around_boat2(row, col, "l")
                    new_board.ROW_counts[row] -= 1
                    new_board.COL_counts[col+1] -= 1
                    new_board.water_row_column(row, col+1)

                elif starting_boat == "t":
                    new_board.grid[row+1][col] = "b"
                    new_board.water_around_boat2(row, col, "t")
                    new_board.COL_counts[col] -= 1
                    new_board.ROW_counts[row+1] -= 1
                    new_board.water_row_column(row+1, col)

                elif starting_boat == "r":
                    new_board.grid[row][col-1] = "l"
                    new_board.water_around_boat2(row, col-1, "l")
                    new_board.ROW_counts[row] -= 1
                    new_board.COL_counts[col-1] -= 1
                    new_board.water_row_column(row, col-1)

                elif starting_boat == ".":
                    if orientation == "down":
                        new_board.grid[row][col] = "t"
                        new_board.grid[row+1][col] = "b"
                        new_board.water_around_boat2(row, col, "t")
                        new_board.COL_counts[col] -= 2
                        new_board.ROW_counts[row] -= 1
                        new_board.ROW_counts[row+1] -= 1
                        new_board.water_row_column(row, col)
                        new_board.water_row_column(row+1, col)

                    elif orientation == "right":
                        new_board.grid[row][col] = "l"
                        new_board.grid[row][col+1] = "r"
                        new_board.water_around_boat2(row, col, "l")
                        new_board.ROW_counts[row] -= 2
                        new_board.COL_counts[col] -= 1
                        new_board.COL_counts[col+1] -= 1
                        new_board.water_row_column(row, col)
                        new_board.water_row_column(row, col+1)
        
                new_board.remaining_boats[2] -= 1

        elif n_action_args == 3:
            row, col, type = action
            if type == "Place boat1":
                new_board.grid[row][col] = "c"
                new_board.water_around_boat1(row, col)
                new_board.COL_counts[col] -= 1
                new_board.ROW_counts[row] -= 1
                new_board.water_row_column(row, col)

                new_board.remaining_boats[3] -= 1

        new_state = BimaruState(new_board)
        #print(new_state.state_id)
        #new_board.print2()

        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        # Se não estiverem colocados todos os barcos
        if not(state.board.remaining_boats[0] == 0 and state.board.remaining_boats[1] == 0 and state.board.remaining_boats[2] == 0 and state.board.remaining_boats[3] == 0):
            return False
    
        # No fim as águas são substituídas por células vazias para melhor visualização da grelha

        for row in range(10):
            for col in range(10):
                if state.board.get_value(row, col) == "w":
                    state.board.grid[row][col] = "."

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

    goal_node.state.board.print2()