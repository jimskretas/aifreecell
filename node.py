from board import Board
from problem import Problem
from typing import List


class Node:
    def __init__(self, board: Board, parent: 'Node' = None, action: List[str] = None, path_cost: int = 0):
        self.board = board
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        self.h_cost = self.__h()

    def __eq__(self, other: 'Node') -> bool:
        """ Two nodes are equal, if their boards are equal. """
        return self.board == other.board

    def __lt__(self, other: 'Node'):
        return self.h_cost < other.h_cost

    def expand(self, problem: Problem) -> List['Node']:
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.board)]

    def child_node(self, problem: Problem, action: List[str]) -> 'Node':
        """ Returns the child node of a node, given an action"""
        next_board = problem.result(self.board, action)
        return Node(next_board, self, action,
                    problem.path_cost(self.path_cost))

    def solution(self) -> List[List[str]]:
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self) -> List['Node']:
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __h(self) -> int:
        """
        Heineman’s Staged Deepening Heuristic(HSDH):  This  is  the  heuristic
        used by the HSD solver. For each foundation pile, locate within the
        cascadepiles the next card that should be placed there, and count
        the cards found on top of it. The returned value is the  sum  of this
        count for all foundations. This number is multiplied by 2
        if there are no available free cells or empty cascade piles
        (reflecting the fact that freeing the next card is harder in this case).
        """
        board = self.board
        # cards_on_top = [0] * 4

        # next_cards = ["%s%s" % (foundation[-1][0], str(int(foundation[-1][1:]) + 1))
        #               for foundation in board.foundations]

        # cards_on_top = [len(stack) - (stack.index(next_card) + 1)
        #                 for next_card in next_cards
        #                 for stack in board.stacks if next_card in stack]

        # for i, foundation in enumerate(board.foundations):
        #     last_card = foundation[-1]
        #     next_card = "%s%s" % (last_card[0], str(int(last_card[1:]) + 1))

        #     for stack in board.stacks:
        #         if next_card in stack:
        #             cards_on_top[i] = len(stack) - (stack.index(next_card) + 1)
        #             break

        # h_cost = sum(cards_on_top) if (0 in board.freecells or []
        #                                in board.stacks) else sum(cards_on_top) * 2
        h_cost = 0

        # To favor foundation moves
        if self.action and self.action[0] == "foundation":
            h_cost -= 1

        empty_freecells = board.freecells.count(0)
        empty_stacks = board.stacks.count([])

        # How many cards are not in foundations
        h_cost += 4 - empty_freecells
        for stack in board.stacks:
            h_cost += len(stack)

        # How many cards can be moved at once
        h_cost -= (2**empty_stacks * (empty_stacks + 1))

        return h_cost
