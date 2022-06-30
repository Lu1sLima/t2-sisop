from abc import abstractmethod
from typing import List

class Alocation:
    """ Classe 'pai' que será herdada pelos diferentes tipos de alocação (polimorfismo)"""

    def __init__(self, capacity: int, verbosity: bool):
        self.capacity = capacity
        self.verbosity = verbosity

    def fit_memory(self, pid: str, from_: int, to: int, stack: List[str]):
        """ Método que adiciona de fato um processo na pilhad e memória,
        comum a todas as classes

        Args:
            pid (str): ID do processo
            from_ (int): início do endereço de memória
            to (int): fim do endereço de memória
            stack (List[str]): pilha de memória
        """
        for i in range(from_, to):
            self.memory_ascii(stack, pid, 'IN', to-from_, i, 'Allocating...')
            stack[i] = pid
        return

    @abstractmethod
    def in_(self):
        """ Método abstrato que deve ser implementado pelas classes que herdarem """
        pass

    @abstractmethod
    def out_(self, pid: str, stack: List[str]) -> None:
        """ Método abstrato que deve ser implementado pelas classes que herdarem """
        pass

    def memory_ascii(self, stack: List[str], pid: str, event: str, psize: int = -1, arrow_idx: int = -1, arrow_suffix: str = '', inputt: bool = True):
        """ Método responsável pelo 'print' da memória no terminal

        Args:
            stack (List[str]): pilha de memória
            pid (str): ID do processo
            event (str): evento ('IN' ou 'OUT')
            psize (int, optional): tamanho do processo. Defaults to -1.
            arrow_idx (int, optional): posição da flecha indicadora. Defaults to -1.
            arrow_suffix (str, optional): label da flecha indicador ('Searching...', 'Alocating...'). Defaults to ''.
            inputt (bool, optional): variável de controle para aparecer o '>>' no terminal. Defaults to True.
        """
        print("\033c")
        print(f'PROCESS ID: {pid}')
        if psize >= 0:
            print(f'PROCESS SIZE: {psize}')
        print(f'PROCESS EVENT: {event}')
        top = '   +' + '-' *9 + '+\n'
        body = ''
        for i, space in enumerate(stack):
            new_str = str(i+1) + ' ' * (3 - len(str(i+1)))
            if space == 'X':
                new_str += '|' + '/' * 9 + '|'
            elif space == 'FREE':
                new_str += '|' + ' ' * 9 + '|'
            else:
                new_str += '|' + ' ' * 4 + space + ' ' *4 + '|'
            
            if i == arrow_idx and self.verbosity:
                new_str += f' <--- {arrow_suffix}'
            body += new_str + '\n'

        bottom = '   +'+ '-'*9 + '+'

        print(top+body+bottom)
        if inputt:
            input('>>')
