from typing import List


class Board:
    def __init__(self, stacks: List[List[str]]):
        self.freecells = [0] * 4
        self.foundations = [['S0'], ['H0'], ['D0'], ['C0']]
        self.stacks = stacks

    def __eq__(self, other: 'Board') -> bool:
        if self.freecells != other.freecells or self.stacks != other.stacks:
            return False
        return True

    def printBoard(self):
        print("Freecells")
        print(self.freecells)

        print("Foundations")
        print(self.foundations)

        print("Stacks")
        print(self.stacks)
