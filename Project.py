import numpy
import search

class BimaruState:
    state_id = 0
    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        #Este método é utilizado em caso de empate na gestão da lista de abertos nas procuras informadas.
        return self.id < other.id

class Board:
    #Representação interna de uma grelha de Bimaru.
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        
        return (self(row-1), self(row+1))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        # TODO
        pass
    #def get_value(self, row:int, col:int) -> (str):


@staticmethod
def parse_instance():
    #Lê a instância do problema do standard input (stdin) e retorna uma instância da classe Board. Por exemplo:
    from sys import stdin
    line = stdin.readline().split()
        
    pass

class Bimaru(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        # TODO
        pass

    def actions(self, state: BimaruState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições da grelha
        estão preenchidas de acordo com as regras do problema. """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass



# Ler a instância a partir do ficheiro 'i1.txt' (Figura 1):
# $ python3 bimaru.py < i1.txt
board = Board.parse_instance()
# Imprimir valores adjacentes
print(board.adjacent_vertical_values(3, 3))
print(board.adjacent_horizontal_values(3, 3))
print(board.adjacent_vertical_values(1, 0))
print(board.adjacent_horizontal_values(1, 0))