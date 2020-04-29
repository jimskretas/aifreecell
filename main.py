import sys
from board import Board
from problem import Problem
from search import depth_first_graph_search, breadth_first_graph_search
from typing import List
import time


def readInput(inputfile: str) -> List[List[str]]:
    try:
        with open(inputfile, "r") as f:
            stacks = [line.split() for line in f]
        return stacks
    except IOError:
        print("Cannot open file:" + inputfile + ". Program terminates.")
        sys.exit(-1)


def writeToFile(outputfile: str, solution: List[List[str]]):
    try:
        with open(outputfile, 'w') as f:
            f.write(str(len(solution)) + '\n')
            f.writelines(" ".join(move) + '\n' for move in solution)
    except IOError:
        print("Cannot open file:" + outputfile + ". Program terminates.")
        sys.exit(-1)


def syntax_msg():
    print("python main.py <method> <input-file> <output-file>")
    print("where: ")
    print("<method> = breadth|depth|best|astar")
    print("<input-file> is a file containing the freecell description.")
    print("<output-file> is the file where the solution will be written.")


def main():
    """
    to run: python main.py <method> <input file> <output file>
    """
    if (len(sys.argv) != 4):
        print("Wrong number of arguments. Use correct syntax:")
        syntax_msg()
        return -1

    methods = {'breadth': 1, 'depth': 2, 'best': 3, 'astar': 4}
    if sys.argv[1] in methods:
        method = methods[sys.argv[1]]
        if(method == 3 or method == 4):
            print("Not implemented")
            return -1
    else:
        print("Wrong method. Use correct syntax:")
        syntax_msg()
        return -1

    stacks = readInput(sys.argv[2])
    board = Board(stacks)
    problem = Problem(board)

    t0 = time.perf_counter()
    if method == 1:
        result = breadth_first_graph_search(problem)
    elif method == 2:
        result = depth_first_graph_search(problem)
    t1 = time.perf_counter()
    print("Time: ", t1 - t0)

    if result:
        writeToFile(sys.argv[3], result.solution())
    else:
        print("Could not solve problem")


if __name__ == "__main__":
    main()
