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

    def __eq__(self, other: 'Node') -> bool:
        """ Two nodes are equal, if their boards are equal. """
        return isinstance(other, Node) and self.board == other.board

    def __lt__(self, other: 'Node'):
        return self.board < other.board

    def expand(self, problem: Problem) -> List['Node']:
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.board)]

    def child_node(self, problem: Problem, action: List[str]) -> 'Node':
        """ Returns the child node of a node, given an action"""
        next_board = problem.result(self.board, action)
        next_node = Node(next_board, self, action, problem.path_cost(
            self.path_cost, self.board, action, next_board))
        return next_node

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
