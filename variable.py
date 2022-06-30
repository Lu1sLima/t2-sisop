import operator
from typing import List
from alocation import Alocation


class Variable(Alocation):
    """ Classe que modela uma gerência de memória variável """

    def __init__(self, alg: str, capacity: int, verbosity: bool = False):
        super().__init__(capacity=capacity, verbosity=verbosity) # Herança
        self.alg = alg
        
    def in_(self, pid: str, psize: int, stack: List[str]) -> None:
        """ Método que modela a entrada de um processo na alocação variável

        Args:
            pid (str): ID do processo
            psize (int): tamanho do processo
            stack (List[str]): pilha de memória
        """

        best_idx, size = -1, float('inf')
        best_idx = -1
        size = float('inf') if self.alg == 'best-fit' else float('-inf')
        comparator = operator.lt if self.alg == 'best-fit' else operator.ge
        i = 0

        while i < len(stack):
            self.memory_ascii(stack, pid, 'IN', psize, i, 'Searching...')
            if stack[i] == 'FREE':
                j = i
                size_so_far = 0
                while j <= len(stack)-1 and stack[j] == 'FREE':
                    size_so_far += 1
                    self.memory_ascii(stack, pid, 'IN', psize, j, 'Searching...')
                    j+=1
                

                self.memory_ascii(stack, pid, 'IN', psize, j if j < len(stack) -1 else j-1, 'Searching...')
                if size_so_far < psize:
                    i = j
                    continue
                
                if comparator(abs(size_so_far - psize), size):
                    size = size_so_far
                    best_idx = i
                i = j
            i += 1

        if best_idx > -1:
            self.fit_memory(pid=pid, from_=best_idx, to=best_idx+psize, stack=stack)
            return
    
        print('INSUFFICIENT MEMORY SPACE!')
        return

    def out_(self, pid: str, stack: List[str]) -> None:
        """ Método que modela a saída de um processo na alocação variável

        Args:
            pid (str): ID do processo
            stack (List[str]): pilha de memória
        """
        
        for i in range(len(stack)):
            self.memory_ascii(stack=stack, pid=pid, event='OUT', arrow_idx=i, arrow_suffix='Searching...')
            if stack[i] == pid:
                j = i
                while stack[j] == pid:
                    self.memory_ascii(stack=stack, pid=pid, event='OUT', arrow_idx=j, arrow_suffix='Cleaning...')
                    stack[j] = 'FREE'
                    j += 1
                return

        print('PROCESS NOT FOUND!')
        return