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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = float(0)
        curr = currentGameState.getFood().asList()
        x, y = newPos
        for m in range(len(newGhostStates)):
            a, b = newGhostStates[m].getPosition()
            moves = abs(x-a) + abs(y-b)
            if newPos in curr:
                score+=1
            if currentGameState.hasWall(x,y):
                score-=2
            if moves <= newScaredTimes[m]:
                score+=moves
            if moves<2:
                score-=2
            dist1 = []
            for c,d in curr:
                dist2 = abs(x-c)
                dist1.append(dist2)
            score-=0.1*min(dist1)
        return score

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        maxVal = -float('inf')
        goal = 0
        for x in range(len(successors)):
            action = self.value(successors[x],1,0)
            if action > maxVal:
                maxVal = action
                goal = x
        return legalActions[goal]
        util.raiseNotDefined()

    def mMax(self, gameState, agent, depth):
        legalActions = gameState.getLegalActions(agent)
        successors = [gameState.generateSuccessor(agent,action) for action in legalActions]
        x = -float('inf')
        for s in successors:
            x = max(x, self.value(s, 1, depth))
        return x

    def mMin(self, gameState, agent, depth):
        legalActions = gameState.getLegalActions(agent)
        successors = [gameState.generateSuccessor(agent,action) for action in legalActions]
        x = float('inf')
        for s in successors:
            if agent+1==gameState.getNumAgents():
                x=min(x, self.value(s,0,depth+1))
            else:
                x=min(x, self.value(s,agent+1,depth))
        return x

    def value(self, gameState, agent, depth):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent==0:
            return self.mMax(gameState,agent,depth)
        if agent>0:
            return self.mMin(gameState,agent,depth)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float('inf')
        beta = float('inf')
        legalActions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0,action) for action in legalActions]
        maxVal = -float('inf')
        goal = 0
        for x in range(len(successors)):
            action = self.value(successors[x],1,0,alpha,beta)
            if action>maxVal:
                maxVal = action
                goal = x
                alpha = action
        return legalActions[goal]
        util.raiseNotDefined()

    def aBMax(self, gameState, agent, depth, alpha, beta):
        legalActions = gameState.getLegalActions(agent)
        x = -float('inf')
        for action in legalActions:
            successor = gameState.generateSuccessor(agent,action)
            x = max(x, self.value(successor,1,depth,alpha,beta))
            if x>beta:
                return x
            alpha = max(alpha,x)
        return x

    def aBMin(self, gameState, agent, depth, alpha, beta):
        legalActions = gameState.getLegalActions(agent)
        x = float('inf')
        for action in legalActions:
            successor = gameState.generateSuccessor(agent,action)
            if agent+1==gameState.getNumAgents():
                x=min(x,self.value(successor,0,depth+1,alpha,beta))
            else:
                x=min(x,self.value(successor,agent+1,depth,alpha,beta))
            if x<alpha:
               return x
            beta = min(beta,x)
        return x

    def value(self, gameState, agent, depth, alpha, beta):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent==0:
            return self.aBMax(gameState, agent, depth, alpha, beta)
        if agent>0:
            return self.aBMin(gameState, agent, depth, alpha, beta)

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
        legalActions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0,action) for action in legalActions]
        maxVal = -float('inf')
        goal = 0
        for x in range(len(successors)):
            action = self.value(successors[x],1,0)
            if action>maxVal:
                maxVal=action
                goal=x
        return legalActions[goal]
        util.raiseNotDefined()

    def eMax(self, gameState, agent, depth):
        legalActions = gameState.getLegalActions(agent)
        successors = [gameState.generateSuccessor(agent,action) for action in legalActions]
        x = -float('inf')
        for successor in successors:
            x = max(x, self.value(successor,1,depth))
        return x

    def eExpected(self, gameState, agent, depth):
        legalActions = gameState.getLegalActions(agent)
        successors = [gameState.generateSuccessor(agent,action) for action in legalActions]
        x = 0.0
        for successor in successors:
            if agent+1==gameState.getNumAgents():
                x+=self.value(successor,0,depth+1)
            else:
                x+=self.value(successor,agent+1,depth)
        return x/len(successors)

    def value(self, gameState, agent, depth):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent==0:
            return self.eMax(gameState,agent,depth)
        if agent>0:
            return self.eExpected(gameState,agent,depth)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodList = food.asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    nearestGhost = 1e9
    for ghostState in ghostStates:
        ghostX, ghostY = ghostState.getPosition()
        ghostX = int(ghostX)
        ghostY = int(ghostY)
        if ghostState.scaredTimer == 0:
            nearestGhost = min(nearestGhost,manhattanDistance((ghostX, ghostY),pos))
        else:
            nearestGhost = -10
    nearestFood = 1e9
    for food in foodList:
        nearestFood = min(nearestFood, manhattanDistance(food, pos))
    if not foodList:
        nearestFood = 0
    return currentGameState.getScore()-7/(nearestGhost+1)-nearestFood/3
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
