from typing import Dict, List

from alocation import Alocation


class Fixed(Alocation):

    def __init__(self, capacity: int, partitions: int, verbosity: bool = False):
        super().__init__(capacity=capacity, verbosity=verbosity)
        self.partitions = partitions
    
    def in_(self, pid: str, psize: int, stack: List[str]) -> None:
        if psize > self.partitions:
            print('INSUFFICIENT MEMORY SPACE')
            input('>>')
            return

        stop = False
        for i in range(0, self.capacity, self.partitions):
            self.memory_ascii(stack, pid, 'IN', psize,i, 'Searching...')
                
            if stack[i] == 'FREE':
                last_diff = len(stack) - i # handle last partition that does not have the full partition amount
                if last_diff < psize:
                    for k in range(last_diff, len(stack)):
                        self.memory_ascii(stack, pid, 'IN', psize, k, 'Searching...')
                    self.memory_ascii(stack, pid, 'IN', psize, k, 'INSUFFICIENT MEMORY SPACE')
                    return

                self.fit_memory(pid=pid, from_=i, to=i+psize, stack=stack)
                j = i+psize
                diff = abs(psize - self.partitions)
                if diff > 0 and j < len(stack)-1: # sobrou espaço
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
