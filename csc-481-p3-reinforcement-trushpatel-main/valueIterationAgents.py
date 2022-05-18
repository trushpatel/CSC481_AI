# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        values = util.Counter()
        for s in states:
            values[(s, 0)] = 0
        for k in range(1, self.iterations + 1):
            for s in states:
                actions = self.mdp.getPossibleActions(s)
                maxV = float('-infinity')
                for a in actions:
                    v = 0
                    nextState = self.mdp.getTransitionStatesAndProbs(s, a)
                    for n in nextState:
                        nS = n[0]
                        p = n[1]
                        r = self.mdp.getReward(s, a, nS)
                        val = values[(nS, k-1)]
                        v += p * (r + self.discount * val)
                    maxV = max(maxV, v)
                if maxV > float('-infinity'):
                    values[(s, k)] = maxV
                else:
                    values[(s, k)] = 0
        for s in states:
            self.values[s] = values[(s, self.iterations)]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        value = 0
        nextState = self.mdp.getTransitionStatesAndProbs(state, action)
        for n in nextState:
            nS = n[0]
            p = n[1]
            r = self.mdp.getReward(state, action, nS)
            v = self.values[nS]
            value += p * (r + self.discount * v)
        return value
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        bestQValue = float('-infinity')
        actions = self.mdp.getPossibleActions(state)
        for a in actions:
            q = self.getQValue(state, a)
            if q > bestQValue:
                bestAction = a
                bestQValue = q
        return bestAction

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for k in range(self.iterations):
            s = states[k % len(states)]
            if s == 'TERMINAL_STATE':
                continue
            actions = self.mdp.getPossibleActions(s)
            maxV = float('-infinity')
            for a in actions:
                value = 0
                nextState = self.mdp.getTransitionStatesAndProbs(s, a)
                for n in nextState:
                    nS = n[0]
                    p = n[1]
                    r = self.mdp.getReward(s, a, nS)
                    v = self.values[nS]
                    value += p * (r + self.discount * v)
                maxV = max(maxV, value)
            if maxV > float('-infinity'):
                self.values[s] = maxV
            else:
                self.values[s] = 0

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        predecessors = {}
        for s in states:
            predecessors[s] = set()
        for s in states:
            for a in self.mdp.getPossibleActions(s):
                nextState = self.mdp.getTransitionStatesAndProbs(s, a)
                for n in nextState:
                    predecessors[n[0]].add(s)

        pQ = util.PriorityQueue()

        for s in states:
            if self.mdp.isTerminal(s):
                continue
            bestAction = self.computeActionFromValues(s)
            highestQ = self.computeQValueFromValues(s, bestAction)
            diff = abs(highestQ - self.values[s])
            pQ.push(s, -diff)

        for i in range(self.iterations):
            if pQ.isEmpty():
                return
            s = pQ.pop()

            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                maxV = float('-infinity')
                for action in actions:
                    value = 0
                    nextState = self.mdp.getTransitionStatesAndProbs(s, action)
                    for n in nextState:
                        nS = n[0]
                        p = n[1]
                        r = self.mdp.getReward(s, action, nS)
                        v = self.values[nS]
                        value += p * (r + self.discount * v)
                    maxV = max(maxV, value)
                if maxV > float('-infinity'):
                    self.values[s] = maxV
                else:
                    self.values[s] = 0

            for p in predecessors[s]:
                bestAction = self.computeActionFromValues(p)
                if bestAction == None:
                    continue
                highestQ = self.computeQValueFromValues(p, bestAction)
                diff = abs(highestQ - self.values[p])

                if diff > self.theta:
                    pQ.update(p, -diff)
