from collections import deque
from board import Board
from node import Node
from problem import Problem
from utils import memoize, PriorityQueue
from typing import Optional


def depth_first_graph_search(problem: Problem) -> Optional[Node]:
    """
    Search the deepest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Does not get trapped by loops.
    If two paths reach a state, only use the first one.
    """
    frontier = [(Node(problem.initial))]  # Stack

    explored = set()
    while frontier:
        # print(len(frontier))
        node = frontier.pop()
        if problem.isSolved(node.board):
            return node
        explored.add(node.board)
        frontier.extend(child for child in node.expand(problem)
                        if child.board not in explored
                        and child not in frontier)
    return None


def breadth_first_graph_search(problem: Problem) -> Optional[Node]:
    """
    Search the shallowest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Does not get trapped by loops.
    """
    node = Node(problem.initial)
    if problem.isSolved(node.board):
        return node
    frontier = deque([node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        node.board.printBoard()
        explored.add(node.board)
        for child in node.expand(problem):
            if child.board not in explored and child not in frontier:
                if problem.isSolved(child.board):
                    return child
                frontier.append(child)
    return None


def best_first_graph_search(problem: Problem, f) -> Optional[Node]:
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.isSolved(node.board):
            return node
        explored.add(node.board)
        for child in node.expand(problem):
            if child.board not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem: Problem, h) -> Optional[Node]:
    """A* search is best-first graph search with f(n) = g(n)+h(n)."""
    h = memoize(h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))
