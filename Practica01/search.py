# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from abc import ABC, abstractmethod

import util


class SearchProblem(ABC):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    @abstractmethod
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    @abstractmethod
    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    @abstractmethod
    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    @abstractmethod
    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    #print("Start:", problem.getStartState())
    #print("Are we in the goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    current = problem.getStartState()
    #print("Current Position:", current)
    visited = []
    
    # store the successors of the start state on a stack as (position, actions)
    stack = [(current, [])]
    #print(f"we have {len(problem.getSuccessors(problem.getStartState()))} successors")
    
    #print("---------- we start the loop ----------")
    while stack:
        current, actions = stack.pop()  # get the last element from the stack
        #print("We move to:", current)

        # check if we reached the goal
        if problem.isGoalState(current):
            #print("Goal found!")
            #print("Actions:", actions)
            return actions

        if current not in visited:
            #print("#################################")
            # add the current node to the visited list
            visited.append(current)
            #print("Visited:", visited)
            #print("We are in:", current)
            #print(f"We have {len(problem.getSuccessors(current))} successors:")
            
            # iterate over successors
            for successor in problem.getSuccessors(current):
                next_position, direction, _ = successor
                if next_position not in visited:
                    # append the successor position and the new action list to the stack
                    new_actions = actions + [direction]
                    stack.append((next_position, new_actions))

            # debug print of the stack
            #for value in stack:
                #print(f"{value} added to the stack")

    #print("Loop finished without finding the goal")
    return []  # return empty if no solution is found



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    current = problem.getStartState()
    visited = []
    
    queue = [(current, [])]
    
    while queue:
        current, actions = queue.pop(0) 

        if problem.isGoalState(current):
            return actions

        if current not in visited:
            visited.append(current)
            
            for successor in problem.getSuccessors(current):
                next_position, direction, _ = successor
                if next_position not in visited:
                    new_actions = actions + [direction]
                    queue.append((next_position, new_actions))

    return []  # return empty if no solution is found

def uniformCostSearch(problem):
    """
    Search the node of least total cost first using a custom PriorityQueue.
    """
    current = problem.getStartState()
    visited = []

    priority_queue = util.PriorityQueue()
    priority_queue.push((current, []), 0) 
    while not priority_queue.isEmpty():
        current, actions = priority_queue.pop()

        if problem.isGoalState(current):
            return actions

        if current not in visited:
            visited.append(current)

            for successor in problem.getSuccessors(current):
                next_position, direction, step_cost = successor
                if next_position not in visited:
                    new_cost = problem.getCostOfActions(actions + [direction])
                    new_actions = actions + [direction]
                    priority_queue.update((next_position, new_actions), new_cost)

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    visited = {}
    solution = []
    queue = util.PriorityQueue()
    parents = {}
    cost = {}

    start = problem.getStartState()
    queue.push((start, 'Undefined', 0), 0)
    visited[start] = 'Undefined'
    cost[start] = 0

    if problem.isGoalState(start):
        return solution

    goal = False;
    while(queue.isEmpty() != True and goal != True):
        node = queue.pop()
        visited[node[0]] = node[1]
        if problem.isGoalState(node[0]):
            node_sol = node[0]
            goal = True
            break
        for elem in problem.getSuccessors(node[0]):
            if elem[0] not in visited.keys():
                priority = node[2] + elem[2] + heuristic(elem[0], problem)
                if elem[0] in cost.keys():
                    if cost[elem[0]] <= priority:
                        continue
                queue.push((elem[0], elem[1], node[2] + elem[2]), priority)
                cost[elem[0]] = priority
                parents[elem[0]] = node[0]

    while(node_sol in parents.keys()):
        node_sol_prev = parents[node_sol]
        solution.insert(0, visited[node_sol])
        node_sol = node_sol_prev

    return solution

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
