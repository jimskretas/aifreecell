from itertools import repeat
import copy
from board import Board
from typing import List


class Problem:
    def __init__(self, initial: Board):
        self.initial = initial

    def __canCardGoThere(self, card1: str, card2: str, foundation: bool = False) -> bool:
        """ Checks if a card can go on top of another card """

        # S (spades, ♠), H (hearts, ♥), D (diamonds, ♦) και C (clubs, ♣)
        # 1 for red, 0 for black
        colors = {'S': 0, 'H': 1, 'D': 1, 'C': 0}
        card1Details = {
            "letter": card1[0],
            "number": int(card1[1:]),
            "color": colors[card1[0]]
        }
        card2Details = {
            "letter": card2[0],
            "number": int(card2[1:]),
            "color": colors[card2[0]]
        }
        if foundation:
            if (card1Details["number"] != card2Details["number"] + 1
                    or card1Details["letter"] != card2Details["letter"]):
                return False
        else:
            if (card1Details["number"] != card2Details["number"] - 1
                    or card1Details["color"] == card2Details["color"]):
                return False
        return True

    def actions(self, board: Board) -> List[str]:
        """Return the actions that can be executed in the given state.

        The possible moves/actions are:
        • freecell card: card moves to an empty freecell.
        • stack card1 card2: card1 goes on top of card2 in a stack
        • newstack card: card moves to an empty stack
        • foundation card: card moves to a foundation
        """
        possible_actions = []
        # contains multiple lists with structure: [ <move>, <card1>, <card2>]
        # move = freecell | stack | newstack | foundation

        # check for cards that can go to a freecell
        if 0 in board.freecells:
            for stack in board.stacks:
                if stack:
                    possible_actions.append(["freecell", stack[-1]])

        # check for cards that can move to another stack
        for card in board.freecells:
            if card != 0:
                for stack in board.stacks:
                    if stack:
                        card2 = stack[-1]
                        if(self.__canCardGoThere(card, card2)):
                            possible_actions.append(["stack", card, card2])
        for stack in board.stacks:
            if stack:
                card = stack[-1]
                for stack2 in board.stacks:
                    if stack2:
                        card2 = stack2[-1]
                        if(self.__canCardGoThere(card, card2)):
                            possible_actions.append(["stack", card, card2])

        # check for cards that can go to an empty stack/new stack
        if [] in board.stacks:
            for card in board.freecells:
                if card:
                    possible_actions.append(["newstack", card])
            for stack in board.stacks:
                if stack:
                    possible_actions.append(["newstack", stack[-1]])

        # check for cards that can go to a foundation
        for card in board.freecells:
            if card != 0:
                for foundation in board.foundations:
                    if(self.__canCardGoThere(card, foundation[-1], True)):
                        possible_actions.append(["foundation", card])
        for stack in board.stacks:
            if stack:
                card = stack[-1]
                for foundation in board.foundations:
                    if(self.__canCardGoThere(card, foundation[-1], True)):
                        possible_actions.append(["foundation", card])

        return possible_actions

    def result(self, state: Board, action: List[str]) -> Board:
        """Return the state that results from executing the given action."""
        board: Board = copy.deepcopy(state)
        move, card1, *card2 = action
        if card2:
            card2 = card2[0]
        foundCard = False

        # First find and remove the card from its original spot
        for i, card in enumerate(board.freecells):
            if card == card1:
                board.freecells[i] = 0
                foundCard = True
                break

        if not foundCard:
            for i, stack in enumerate(board.stacks):
                if stack and card1 == stack[-1]:
                    board.stacks[i].pop()

        # Then place the card where it should go
        if move == 'freecell':
            index = board.freecells.index(0)
            board.freecells[index] = card1
        elif move == 'newstack':
            index = board.stacks.index([])
            board.stacks[index].append(card1)
        elif move == 'foundation':
            cardLetter = card1[0]
            for i, stack in enumerate(board.foundations):
                if stack[-1][0] == cardLetter:
                    board.foundations[i].append(card1)
                    break
        elif move == 'stack':
            for i, stack in enumerate(board.stacks):
                if stack and stack[-1] == card2:
                    board.stacks[i].append(card1)
                    break
        else:
            print("wrong move")

        return board

    def isSolved(self, board: Board) -> bool:
        """
        Checks if a game is solved.

        Game is solved when all the cards are in foundations
        and therefore freecells and stacks are empty.
        """
        if(board.freecells != [0, 0, 0, 0]):
            return False
        for stack in board.stacks:
            if stack:
                return False
        return True
