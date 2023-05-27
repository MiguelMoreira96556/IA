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


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    

    


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, grid):
        self.grid = grid

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        
        return self.grid[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): #check if values are within bounds
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""

        if row == 0:
            return ("None", self.grid[row+1][col])
        
        elif row == 9:
            return (self.grid[row-1][col], "None")
        
        else:
            return self.grid[row-1][col], self.grid[row+1][col]

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if col == 0:
            return ("None", self.grid[row][col+1])
        
        elif col == 9:
            return (self.grid[row][col-1], "None")
        
        return self.grid[row][col-1], self.grid[row][col+1]

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board. """

        from sys import stdin
        
        ROW = stdin.readline().split()     #lè a 1ª linha do ficheiro
        COLUMN = stdin.readline().split()  #lè a 2ª linha do ficheiro

        ROW_counts = [int(ship_count) for ship_count in ROW[1:]] #lè ROW desde o 2º elemento até ao último na forma int
        COLUMN_counts = [int(ship_count) for ship_count in COLUMN[1:]]

        grid = [['.' for _ in range(10)] for _ in range(10)]   #cria uma matriz 10x10 vazia

        Nhints = int(stdin.readline())

        for _ in range(Nhints):
            hint_line = stdin.readline().split()
            row = int(hint_line[1])
            col = int(hint_line[2])
            ship_type = hint_line[3]
            grid[row][col] = ship_type

        return Board(grid)


        #i = 0
        #lines = []
        #Row = []
        #Column = []
        #Hints = []
        #for line in stdin:
        #    line = line.split()
        #    lines.append(line)
        #    j = 0
        #    for pos in line:
        #        if i == 0: #guardar a ROW
        #            if j != 0:
        #                Row.append(pos)
        #
        #        elif i == 1: #guardar a COLUMN
        #            if j != 0:
        #                Column.append(pos)
        #
        #        elif i == 2: #guardar nº hints
        #            Nhints = pos
        #
        #        else:
        #            Hints.append(pos)
        #
        #
        #        j = j + 1
        #            
        #    i = i + 1

    def w(self, row: int, col: int): #neste momento a água está como "w". No fim tem de estar como "."
        self.grid[row][col] = "w"

    def c(self, row: int, col: int):
        self.grid[row][col] = "c"

    def t(self, row: int, col: int):
        self.grid[row][col] = "t"

    def m(self, row: int, col: int):
        self.grid[row][col] = "m"

    def b(self, row: int, col: int):
        self.grid[row][col] = "b"

    def t(self, row: int, col: int):
        self.grid[row][col] = "l"

    def r(self, row: int, col: int):
        self.grid[row][col] = "r"

    def print(self):
        for row in self.grid:
            print(" ".join(row))







class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial_state = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        return ["place_water"]

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        row, col, ship_type = action
        grid_copy = state.board.grid.copy()
        grid_copy[row][col] = ship_type
        new_state = BimaruState(Board(grid_copy))

        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":

    board = Board.parse_instance()

    # Criar uma instância de Bimaru:
    problem = Bimaru(board)

    # Criar um estado com a configuração inicial:
    initial_state = BimaruState(board)

    # Mostrar valor na posição (3, 3):
    print(initial_state.board.get_value(0, 0))

    # Realizar acção de inserir o valor w (água) na posição da linha 3 e coluna 3
    result_state = problem.result(initial_state, (3, 3, "w"))

    board.print()