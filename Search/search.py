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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #util.raiseNotDefined()
    '''
        Remember that a search node must contain not only a state but also
        the information necessary to reconstruct the path (plan) which gets to that state.
    '''
    list_of_actions = util.Stack() # will contain the stack that the function will return
    explored = util.Stack() # to keep track of explored nodes
    stack = util.Stack() # Fringe is a LIFO stack
    stack.push((problem.getStartState(), []))

    # follow the pseudocode provided in the lecture notes
    while not stack.isEmpty():
        (node, path) = stack.pop()
        if problem.isGoalState(node):
            list_of_actions = path
            break

        if node not in explored.list:
            explored.push(node)
            for w in problem.getSuccessors(node):
                new_path = path + [w[1]]
                new_node = (w[0], new_path) # expand
                stack.push(new_node)

    # return a list of ​actions​ that will lead the agent from the start to the goal.
    return list_of_actions
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    list_of_actions = util.Queue()
    explored = util.Queue()
    queue = util.Queue() # Fringe is a FIFO queue
    queue.push((problem.getStartState(), []))

    while not queue.isEmpty():
        (node, path) = queue.pop()
        if problem.isGoalState(node):
            list_of_actions = path
            break

        if node not in explored.list:
            explored.push(node)
            for w in problem.getSuccessors(node):
                new_path = path + [w[1]]
                new_node = (w[0], new_path) # expand
                queue.push(new_node)

    return list_of_actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    list_of_actions = util.Queue()
    explored = util.Queue()
    priority_queue = util.PriorityQueue() # Fringe is a priority queue
    priority_queue.update((problem.getStartState(), [], 0),0)

    while not priority_queue.isEmpty():
        (node, path, path_cost) = priority_queue.pop()
        if problem.isGoalState(node):
            list_of_actions = path
            break

        if node not in explored.list:
            explored.push(node)
            for w in problem.getSuccessors(node):
                new_path = path + [w[1]]
                newCost = path_cost + w[2]
                new_node = (w[0], new_path, newCost) # expand
                priority_queue.update(new_node, newCost)

    return list_of_actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    list_of_actions = util.Queue()
    explored = util.Queue() 
    priority_queue = util.PriorityQueue() # Fringe is a priority queue
    priority_queue.update((problem.getStartState(), [], 0), 0)

    while not priority_queue.isEmpty():
        (node, path, path_cost) = priority_queue.pop()
        if problem.isGoalState(node):
            list_of_actions = path
            break
        # before expanding a node, check to make sure its state has never been expanded before
        # if not new, skip it, if new add to closed set(the puts its childeren into fridge)
        if node not in explored.list: 
            explored.push(node)
            for w in problem.getSuccessors(node):
                new_path = path + [w[1]]
                newCost = path_cost + w[2] # S(0+2)
                new_node = (w[0], new_path, newCost)
                # A* Search orders by the sum: f(n) = g(n) + h(n)
                # g = backward cost, h = forward cost
                priority_queue.update(new_node, newCost+heuristic(w[0],problem))

    return list_of_actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
