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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    visited = set() #keep track of visited nodes 
    state = problem.getStartState()
    path = []
    fringe.push((state, path))     
    while not fringe.isEmpty():
        state , path = fringe.pop()
        if problem.isGoalState(state)  :
            return path # goal is reached 
        if state not in visited :
            visited.add(state) #visited state marked  
            succesors = problem.getSuccessors(state) #fetch succesors list  (triplet)
            for i in succesors :
                successor = i[0]
                action = i[1]
                fringe.push((successor, path + [action]))
    return path
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    fringe = util.Queue() 
    visited = set()
    startState = problem.getStartState()
    fringe.push((startState, []))  # (state, path)

    while not fringe.isEmpty():
        state, path = fringe.pop()
        if problem.isGoalState(state):
            return path
        if state not in visited:
            visited.add(state)  # mark the state as visited
            succesors = problem.getSuccessors(state) #fetch succesors 
            for i in succesors :
                successor = i[0]
                action = i[1]
                fringe.push((successor, path + [action]))
    return [] 


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    fringe = util.PriorityQueue()
    visited = {}  #track the min cost for each visited node
    startState = problem.getStartState()
    fringe.push((startState, [], 0), 0)  # (state, path, cost) 

    while not fringe.isEmpty():
        state, path, cost = fringe.pop()
        if problem.isGoalState(state):
            return path  

        # Only process the state if it's not visited or found with a lower cost
        unvisited = float("inf")
        if cost < visited.get(state, unvisited):
            visited[state] = cost  # update with the min cost to reach this state
            for i in problem.getSuccessors(state):
                updateCost = cost + i[2]  
                if updateCost < visited.get(i[0], unvisited):
                    fringe.push((i[0], path + [i[1]], updateCost), updateCost)

    return []  # Return an empty list if no path to the goal is found


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue() 
    startState = problem.getStartState()
   
    fringe.push((startState, [], 0), heuristic(startState, problem))  # (state, path, cost) priority equal to the heuristic
    visited = {}  # track visited nodes with min cost

    while not fringe.isEmpty():
        current_state, current_path, current_cost = fringe.pop()

        if problem.isGoalState(current_state):
            return current_path  

        if current_state not in visited or current_cost < visited[current_state]:
            visited[current_state] = current_cost  # Update the minimum cost to reach this state

            for successor, action, stepCost in problem.getSuccessors(current_state):
                newCost = current_cost + stepCost
                priority = newCost + heuristic(successor, problem)  # f(n) = g(n) + h(n)
                if successor not in visited or newCost < visited.get(successor, float('inf')):
                    fringe.push((successor, current_path + [action], newCost), priority)  
    return [] #empty if no solution
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
