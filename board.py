from typing import List


class Board:
    def __init__(self, stacks: List[List[str]], freecells: List[int] = [0] * 4, foundations: List[List[str]] = [['S0'], ['H0'], ['D0'], ['C0']]):
        self.freecells = freecells
        self.foundations = foundations
        self.stacks = stacks

    def __eq__(self, other: 'Board') -> bool:
        if self.freecells != other.freecells or self.stacks != other.stacks:
            return False
        return True

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        state = tuple([card for stack in self.stacks for card in stack])
        return hash(state)

    def __copy__(self):
        new_foundations = [[card for card in foundation]
                           for foundation in self.foundations]
        new_freecells = [card for card in self.freecells]
        new_stacks = [[card for card in stacks]
                      for stacks in self.stacks]
        return Board(new_stacks, new_freecells, new_foundations)

    def printBoard(self):
        print("Freecells")
        print(self.freecells)

        print("Foundations")
        print(self.foundations)

        print("Stacks")
        print(self.stacks)
