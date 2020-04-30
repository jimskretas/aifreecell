from typing import List
from operator import add
from functools import reduce


class Board:
    def __init__(self, stacks: List[List[str]]):
        self.freecells = [0] * 4
        self.foundations = [['S0'], ['H0'], ['D0'], ['C0']]
        self.stacks = stacks

        cards_left = 0
        for stack in self.stacks:
            cards_left += len(stack)
        for card in self.foundations:
            if card != 0:
                cards_left += 1
        self.cards_left = cards_left

    def __eq__(self, other: 'Board') -> bool:
        if self.freecells != other.freecells or self.stacks != other.stacks:
            return False
        return True

    def __lt__(self, other: 'Board') -> bool:
        return isinstance(other, Board) and self.cards_left < other.cards_left

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        state = tuple([card for stack in self.stacks for card in stack])
        return hash(state)

    def printBoard(self):
        print("Freecells")
        print(self.freecells)

        print("Foundations")
        print(self.foundations)

        print("Stacks")
        print(self.stacks)
