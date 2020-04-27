from collections import deque
from board import Board
from node import Node
from problem import Problem
from typing import Optional


def depth_first_graph_search(problem: Problem) -> Optional[Node]:
    frontier = [(Node(problem.initial))]  # Stack

    explored = []
    while frontier:
        node = frontier.pop()
        if problem.isSolved(node.board):
            return node
        explored.append(node.board)
        frontier.extend(child for child in node.expand(problem)
                        if child.board not in explored
                        and child not in frontier)
    return None


def breadth_first_graph_search(problem: Problem) -> Optional[Node]:
    node = Node(problem.initial)
    if problem.isSolved(node.board):
        return node
    frontier = deque([node])
    explored = []
    while frontier:
        node = frontier.popleft()
        explored.append(node.board)
        for child in node.expand(problem):
            if child.board not in explored and child not in frontier:
                if problem.isSolved(child.board):
                    return child
                frontier.append(child)
    return None
