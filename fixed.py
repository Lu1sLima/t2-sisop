from typing import Dict, List

from alocation import Alocation


class Fixed(Alocation):
    """ Classe que modela uma alocação FIXA (com partições) """

    def __init__(self, capacity: int, partitions: int, verbosity: bool = False):
        super().__init__(capacity=capacity, verbosity=verbosity) # Herança
        self.partitions = partitions
    
    def in_(self, pid: str, psize: int, stack: List[str]) -> None:
        """ Método que modela a entrada de um processo na alocação fixa com partição

        Args:
            pid (str): ID do processo
            psize (int): tamanho do processo
            stack (List[str]): pilha de memória
        """

        # se o processo for maior que a partição
        # como conversado por email, não foi implementado a paginação ...
        # ... se o processo for maior do que a partição
        if psize > self.partitions:
            self.memory_ascii(stack, pid, 'IN', psize, 0, 'PROCESS SIZE BIGGER THAN FRAME SIZE!')
            print('INSUFFICIENT MEMORY SPACE')
            input('>>')
            return

        stop = False
        for i in range(0, self.capacity, self.partitions):
            self.memory_ascii(stack, pid, 'IN', psize,i, 'Searching...')
                
            if stack[i] == 'FREE':
                last_diff = len(stack) - i
                if last_diff < psize:
                    for k in range(last_diff, len(stack)):
                        self.memory_ascii(stack, pid, 'IN', psize, k, 'Searching...')
                    self.memory_ascii(stack, pid, 'IN', psize, k, 'INSUFFICIENT MEMORY SPACE')
                    return

                self.fit_memory(pid=pid, from_=i, to=i+psize, stack=stack)
                j = i+psize
                diff = abs(psize - self.partitions)
                if diff > 0 and j < len(stack)-1: # sobrou espaço, coloca X na frag. interna
                    for j in range(i+psize, i+psize+diff):
                        self.memory_ascii(stack, pid, 'IN', psize,j, 'Internal fragmentation...')
                        stack[j] = 'X'
                
                stop = True
            
            if stop:
                return
        
        print('INSUFFICIENT MEMORY SPACE')
        input('>>')
        return

    def out_(self, pid: str, stack: List[str]) -> None:
        """ Método que modela a saída de um processo na partição FIXA

        Args:
            pid (str): ID do processo
            stack (List[str]): pilha de memória
        """

        for i in range(0, self.capacity, self.partitions):
            self.memory_ascii(stack=stack, pid=pid, event='OUT', arrow_idx=i, arrow_suffix='Searching...')

            if stack[i] == pid:
                for j in range(i, i+self.partitions):
                    self.memory_ascii(stack=stack, pid=pid, event='OUT', arrow_idx=j, arrow_suffix='Cleaning...')
                    if j > len(stack)-1:
                        break
                    stack[j] = 'FREE'
                return

        print('PROCESS NOT FOUND!')
        return        
