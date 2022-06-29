import json
import argparse

from typing import Dict, List

from fixed import Fixed
from utils import memory_ascii
from variable import Variable

class MemoryManager:

    def __init__(self, processes: List[Dict], capacity: int, partitions: int, alg: str, typee: str, verbosity: bool = False):
        self.stack: List[str] = ['FREE'] * capacity
        self.capacity: int = capacity
        self.partitions: int = partitions
        self.alg: int = alg
        self.processes: List[Dict] = processes
        self.type = typee
        self.verbosity = verbosity

    def run(self):
        type_mapper = {
            'fixed': Fixed(capacity=self.capacity, verbosity=self.verbosity, partitions=self.partitions),
            'variable': Variable(alg='best-fit', capacity=self.capacity, verbosity=self.verbosity)
            }

        for process in self.processes:
            event, pid, psize = process.values()
            if event == 'IN':
                type_mapper[self.type].in_(pid, psize, self.stack)
            else:
                type_mapper[self.type].out_(pid, self.stack)
        type_mapper[self.type].memory_ascii(stack=self.stack, pid=pid, psize=-1, event=event, inputt=False)

            

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('file_path', type=str, help="input file path")
    # parser.add_argument('-v', '--verbosity', action='store_true', help="show where the algorithm is searching/alocation in the memory", required=False)
    # args = parser.parse_args()

    filepath = 'input2.json'

    with open(filepath, 'r') as file:
        content = json.loads(file.read())
        mem = MemoryManager(**content, verbosity=True)

    mem.run()