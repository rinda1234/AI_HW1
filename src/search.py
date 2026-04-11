import inspect
import sys
import random
import heapq
from collections import deque
import time

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)


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
        pass

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        pass

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        pass

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        pass

# 예시용 탐색 알고리즘
def random_search(problem): 
    """
    Search the nodes in the search tree randomly.

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm.

    This random_search function is just example not a solution.
    You can write your code by examining this function
    """
    start = problem.getStartState()
    node = [(start, "", 0)] 
    frontier = [node]
    frontier_states = {start} 
    explored = set() 

    while frontier:
        node_index = random.randrange(len(frontier)) 
        node = frontier.pop(node_index) 
        state = node[-1][0] 
        frontier_states.discard(state) 

        if problem.isGoalState(state): 
            return [x[1] for x in node][1:]

        if state not in explored: 
            explored.add(state) 
            for successor in problem.getSuccessors(state): 
                if successor[0] not in explored and successor[0] not in frontier_states:
                    parent = node[:]
                    parent.append(successor) 
                    frontier.append(parent) 
                    frontier_states.add(successor[0])

    return []


def depth_first_search(problem):
  
    start_time = time.time()
    start = problem.getStartState() 
    node = [(start, "", 0)] 
    frontier = [node]
    frontier_states = {start} 
    explored = set() 
    
    while frontier:
        node = frontier.pop() 
        state = node[-1][0] 
        frontier_states.discard(state)  

        if problem.isGoalState(state): 
            end_time = time.time()
            print(f"DFS: {end_time - start_time:.6f} seconds")
            return [x[1] for x in node][1:] 
        
        if state not in explored: 
            explored.add(state) 
            for successor in problem.getSuccessors(state):
                 if successor[0] not in explored and successor[0] not in frontier_states:
                    parent = node[:] 
                    parent.append(successor) 
                    frontier.append(parent) 
                    frontier_states.add(successor[0])

    return []



def breadth_first_search(problem):

    start_time = time.time()
    start = problem.getStartState()
    node = [(start, "", 0)] 
    frontier = deque([node])
    frontier_states = {start}
    explored = set() 

    while frontier:
        node = frontier.popleft() 
        state = node[-1][0] 
        frontier_states.discard(state) 

        if problem.isGoalState(state): 
            end_time = time.time()
            print(f"BFS: {end_time - start_time:.6f} seconds")
            return [x[1] for x in node][1:]
 
        if state not in explored: 
            explored.add(state) 
            for successor in problem.getSuccessors(state):
                if successor[0] not in explored and successor[0] not in frontier_states:
                    parent = node[:]
                    parent.append(successor)
                    frontier.append(parent)
                    frontier_states.add(successor[0])

    return []


def uniform_cost_search(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_time = time.time()


    start = problem.getStartState() 
    node = [(start, "", 0)] 
    frontier = []
    heapq.heappush(frontier, (0, 0, node)) 

    frontier_states = {start: 0}
    explored = set() 
    count = 0 

    while frontier:
        cost, _, node = heapq.heappop(frontier)
        state = node[-1][0] 
        
        if problem.isGoalState(state): 
            end_time = time.time()
            print(f"UCS: {end_time - start_time:.6f} seconds")
            return [x[1] for x in node][1:]
        
        if state not in explored: 
            explored.add(state) 
            frontier_states.pop(state, None) 
            for successor in problem.getSuccessors(state):
                if successor[0] not in explored: 
                    if successor[0] not in frontier_states or frontier_states[successor[0]] > cost + successor[2]: 
                        parent = node[:]
                        parent.append(successor)
                        heapq.heappush(frontier, (cost + successor[2], count, parent))
                        frontier_states[successor[0]] = cost + successor[2]
                        count += 1

        

    return []


def heuristic(state, problem=None):


    result = 0
    for row in range(3): 
            for col in range(3):
                if state.cells[row][col] != 0:
                    result += abs((state.cells[row][col] - 1) // 3 - row) + abs((state.cells[row][col] - 1) % 3 - col)

    
    return result

    


def aStar_search(problem, heuristic=heuristic):

    start_time = time.time()
    start = problem.getStartState() 
    node = [(start, "", 0)] 
    frontier = []
    g = 0;
    f = 0;
    heapq.heappush(frontier, (f, 0, g, node)) 
   
    frontier_states = {start: 0}
    explored = set() 
    count = 0 

    while frontier:
        _, _, g, node = heapq.heappop(frontier)
        state = node[-1][0] 

        
        if problem.isGoalState(state):
            end_time = time.time()
            print(f"A*: {end_time - start_time:.6f} seconds")
            return [x[1] for x in node][1:]
        
        if state not in explored: 
            explored.add(state) 
            frontier_states.pop(state, None) 
            for successor in problem.getSuccessors(state):
                if successor[0] not in explored: 
                    h = heuristic(successor[0], problem) 
                    child_g = g + successor[2] 
                    f = child_g + h 
                    if successor[0] not in frontier_states or frontier_states[successor[0]] > child_g: 
                        parent = node[:]
                        parent.append(successor)
                        heapq.heappush(frontier, (f, count, child_g, parent)) 
                        frontier_states[successor[0]] =  child_g
                        count += 1                                              

    return []


rand = random_search
bfs = breadth_first_search
dfs = depth_first_search
astar = aStar_search
ucs = uniform_cost_search
