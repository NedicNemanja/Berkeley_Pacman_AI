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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        #list of scaredTimer for every ghost that counts to 0, when 0 ghost is no longer scared
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        eval = successorGameState.getScore()

        #food related
        food_weight = 2
        for food in newFood.asList():
            food_proximity = 1.0/manhattanDistance(newPos,food)
            eval = eval + food_weight*food_proximity
        #ghost related
        ghost_dist_weight = -7
        scared_ghost_weight = 10
        for ghost in newGhostStates:
            if ghost.scaredTimer > 0:   #chase ghosts
                eval += scared_ghost_weight*(1.0/(manhattanDistance(newPos,ghost.getPosition())+0.01))
            else:   #run away from ghosts
                eval += ghost_dist_weight*(1.0/(manhattanDistance(newPos,ghost.getPosition())+0.01))
        return eval

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

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
        def RecursiveMinimax(agent, gameState, level):
            """ Returns the score of the agent for gameState.
                level is depth*numofAgents. i.e: if depth=2 and we have 3 agents the first level is 6 and the last is 1
                at every recursion the level is decreased by one until we get to level==1.
            """
            if level==1 or gameState.isLose() or gameState.isWin(): #BASE CASE last level
                return self.evaluationFunction(gameState)

            if agent==0: #MAX aka pacman
                result = -float('inf')
                #get score for every action, and return max score
                for action in gameState.getLegalActions(agent):
                    result = max(result, RecursiveMinimax((agent+1)%gameState.getNumAgents(),\
                                                        gameState.generateSuccessor(agent,action),\
                                                        level-1))
                return result
            else:       #Ghost
                result = float('inf')
                #get score for every action and return min score
                for action in gameState.getLegalActions(agent):
                    result = min(result, RecursiveMinimax((agent+1)%gameState.getNumAgents(),\
                                                        gameState.generateSuccessor(agent,action),\
                                                        level-1))
                return result

        #For MAX find the best action (action with max score) and return it
        Max = -float('inf')
        for action in gameState.getLegalActions():
            result = RecursiveMinimax(1,gameState.generateSuccessor(0,action),self.depth*gameState.getNumAgents())
            if result > Max:
                Max = result
                max_action = action
        return max_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def RecursiveABPruning(agent, gameState, level, alpha, beta):
            """ Returns the score of the agent for gameState.
                level is depth*numofAgents. i.e: if depth=2 and we have 3 agents the first level is 6 and the last is 1
                at every recursion the level is decreased by one until we get to level==1.
            """
            #print agent,alpha, beta
            if level==1 or gameState.isLose() or gameState.isWin(): #BASE CASE last level
                return self.evaluationFunction(gameState)

            if agent==0: #MAX aka pacman
                result = -float('inf')
                #get score for every action, and return max score
                for action in gameState.getLegalActions(agent):
                    result = max(result, RecursiveABPruning((agent+1)%gameState.getNumAgents(),\
                                                        gameState.generateSuccessor(agent,action),\
                                                        level-1,alpha,beta))
                    if result > beta:
                        #print result
                        return result
                    alpha = max(alpha,result)
                #print result
                return result
            else:   #Ghost
                result = float('inf')
                #get score for every action and return min score
                for action in gameState.getLegalActions(agent):
                    result = min(result, RecursiveABPruning((agent+1)%gameState.getNumAgents(),\
                                                        gameState.generateSuccessor(agent,action),\
                                                        level-1,alpha,beta))
                    if result < alpha:
                        #print result
                        return result
                    beta = min(beta,result)
                #print result
                return result

        #For MAX find the best action (action with max score) and return it
        # alpha-beta bounds
        alpha = -float('inf')
        beta = float('inf')
        Max = -float('inf')
        for action in gameState.getLegalActions():
            result = RecursiveABPruning(1,gameState.generateSuccessor(0,action),self.depth*gameState.getNumAgents(),
                                        alpha,beta)
            if result > Max:
                Max = result
                max_action = action
            if Max > beta:
                #print Max
                return max_action
            alpha = max(alpha, Max)
        #print alpha,beta
        return max_action

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
        def RecursiveExpectimax(agent,gameState, level):
            """ Returns the score of the agent for gameState.
                level is depth*numofAgents. i.e: if depth=2 and we have 3 agents the first level is 6 and the last is 1
                at every recursion the level is decreased by one until we get to level==1.
            """
            if level==1 or gameState.isLose() or gameState.isWin(): #BASE CASE last level
                return self.evaluationFunction(gameState)

            if agent==0: #MAX aka pacman
                result = -float('inf')
                # get score for every action, and return max score
                for action in gameState.getLegalActions(agent):
                    result = max(result, RecursiveExpectimax((agent+1)%gameState.getNumAgents(),\
                                                        gameState.generateSuccessor(agent,action),\
                                                        level-1))
                return result
            else:       #chance node
                result = 0.0
                probability = 1.0/len(gameState.getLegalActions(agent)) #uniform distribution
                # get score for every action, and return max score
                for action in gameState.getLegalActions(agent):
                    result += probability * RecursiveExpectimax((agent+1)%gameState.getNumAgents(),\
                                                        gameState.generateSuccessor(agent,action),\
                                                        level-1)
                #print result
            return result

        #For MAX find the best action (action with max score) and return it
        Max = -float('inf')
        for action in gameState.getLegalActions():
            result = RecursiveExpectimax(1,gameState.generateSuccessor(0,action),self.depth*gameState.getNumAgents())
            if result > Max:
                Max = result
                max_action = action
        return max_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
        Score feature: add currentGameState score
        Food feature: weight*inverse_distance-to_nearest-food
        Ghost features:
            ghost: negative_weight*inverse-distance-to-nearest-ghost
            scared ghost: weight*inverse-distance-to-nearest-ghost
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    eval = currentGameState.getScore()

    # food related
    food_weight = 5
    min_food_dist = float('inf')
    for food in newFood.asList():
        min_food_dist = min(min_food_dist,manhattanDistance(newPos, food))
    eval += food_weight * 1.0/min_food_dist

    # ghost related
    ghost_dist_weight = -7
    scared_ghost_weight = 13
    # find nearest ghost
    min_ghost_distance = float('inf')
    for ghost in newGhostStates:
        min_ghost_distance = min(min_ghost_distance,manhattanDistance(newPos, ghost.getPosition()))
    #evaluate that ghost based on if hes scared or not
    if ghost.scaredTimer > 0:  # chase ghosts
        eval += scared_ghost_weight * (1.0 / (min_ghost_distance + 0.01))
    else:  # run away from ghosts
        eval += ghost_dist_weight * (1.0 / (min_ghost_distance + 0.01))
    #print eval
    return eval

# Abbreviation
better = betterEvaluationFunction

