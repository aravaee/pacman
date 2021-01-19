# multiAgents.py
# --------------
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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        inf = float('inf') # infinity 
        ghost_pos = successorGameState.getGhostPositions() # get ghost position

        # to keep the ghost away from pacman we have to have a minimum distance of 2
        # To avoid the ghost, we assign the lowest score, negative infinity, to the state
        for pos in ghost_pos:
            if manhattanDistance(newPos, pos) < 2:
              return -inf

        # to eat food, we do not have to worry about the ghost, since it will be avoided as designed above
        num_food = currentGameState.getNumFood()
        new_num_food = successorGameState.getNumFood()
        if new_num_food < num_food:
          return inf

        # assign score based on how close the food is, this will help pacman to find the food (or get closer to it)
        min_distance = inf
        for food in newFood.asList():
          distance = manhattanDistance(newPos, food)
          min_distance = min(min_distance, distance)

        return 1/min_distance

        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax_helper agent (question 2)
    """

    def min_value(self, agent, gameState, depth):
        current_best_value = float("inf")  # highest possible value

        # loop through all the legal actions of the agent (pacman or ghosts)
        for action in gameState.getLegalActions(agent):
          suc = gameState.generateSuccessor(agent, action)  # successor
          value = self.minimax_helper(suc, agent + 1, depth)
          # pick the min of current best and value
          current_best_value = min(current_best_value, value)
        return current_best_value

    def max_value(self, agent, gameState, depth):
        current_best_value = float("-inf")  # lowest possible value

        # loop through all the legal actions of the agent (pacman or ghosts)
        for action in gameState.getLegalActions(agent):
          suc = gameState.generateSuccessor(agent, action)  # successor
          # check for the next agent
          value = self.minimax_helper(suc, agent + 1, depth)
          # pick the max of current best and value
          current_best_value = max(current_best_value, value)

          # Final action, that performs at depth 1, is saved
          if depth == 1 and current_best_value == value:
              self.action = action
        return current_best_value

    def minimax_helper(self, gameState, agent=0, depth=0):

        # to keep the agent index in range, we can get modules of number of agents, then we can increment the agent index by one
        agent = agent % gameState.getNumAgents()

        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)

        if agent == 0:  # maximize for pacman
          # calculate the next agent and increment the depth accordingly
          if depth < self.depth:
            return self.max_value(agent, gameState, depth+1)
          else:
            return self.evaluationFunction(gameState)
        else:  # minimize for ghosts
          return self.min_value(agent, gameState, depth)

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        self.minimax_helper(gameState)
        return self.action

        #util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
