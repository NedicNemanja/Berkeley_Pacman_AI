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

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

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
    return  [s, s, w, s, w, w, s, w]

def dfs_recursive(problem, curr_node, visited, path):
    if problem.isGoalState(curr_node):   #BASE CASE
        return True
    #else if not goal, expand successors and search for goal in them
    visited.add(curr_node)
    for child in problem.getSuccessors(curr_node):
        if child[0] not in visited:                 #check all unvisited successors
            if dfs_recursive(problem, child[0], visited, path):
                path.insert(0,child[1])
                return True #goal is a successor of this child
    return False #none of curr_node successors lead to the goal

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    path = []
    if not dfs_recursive(problem, problem.getStartState(), visited, path):
        print "dfs failed to find a GoalState"
    return path
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    queue = Queue()
    visited = set()
    path = []

    start = problem.getStartState()
    queue.push([start, path])  # queue's elements will look like this: (node,[path_to_this_node])
    visited.add(start)

    while not queue.isEmpty():
        curr_node = queue.pop()

        if problem.isGoalState(curr_node[0]):
            return curr_node[1]  # return path to goal
        else:
            for child in problem.getSuccessors(curr_node[0]):
                if child[0] not in visited:  # for every unvisited child
                    new_path = list(curr_node[1])   #tell this child how it got here
                    new_path.append(child[1])
                    queue.push((child[0], new_path))
                    visited.add(child[0])
    print "bfs failed to find GoalState"
    return path
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    visited = set()
    path = []
    pqueue = PriorityQueue()                           #priority queue will be based on least path cost
    pqueue.push( (problem.getStartState(),path,0), 0 ) #pqueue element: (position,path to position,total cost)

    while not pqueue.isEmpty():
        curr_node = pqueue.pop()    #choose node with least cost

        if curr_node[0] in visited:
            continue

        visited.add(curr_node[0])
        if problem.isGoalState(curr_node[0]):
            return curr_node[1] #found goal, returning optimal path
        else:
            for child in problem.getSuccessors(curr_node[0]):   #expand/update frontier
                if child[0] not in visited:
                    new_cost = curr_node[2]+child[2]    #parent cost + cost
                    new_path = list(curr_node[1])
                    new_path.append(child[1])           #parent path + action
                    pqueue.update( (child[0],new_path,new_cost), new_cost)
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
