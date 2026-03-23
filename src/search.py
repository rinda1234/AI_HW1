import inspect
import sys
import random
import heapq
from collections import deque


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
# 시작상태반환
    def getStartState(self): 
        """
        Returns the start state for the search problem.
        """
        pass
# 목표상태인지 확인
    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        pass
# 다음 상태들 반환 (successor, action, stepCost) 튜플의 리스트로 반환. successor는 다음 상태, action은 그 상태로 가기 위한 행동, stepCost는 그 행동의 비용
    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        pass
# 행동 리스트 전체 비용 계산. 모든 행동비용이 1이므로, 총비용 = 행동 개수.
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
    start = problem.getStartState() # 시작 상태 가져옴
    node = [(start, "", 0)] # 노드 초기화. 노드는 (상태, 행동, 비용) 튜플의 리스트. 처음에는 시작 상태만 포함. 행동은 빈 문자열, 비용은 0으로 초기화.
    frontier = [node]# 앞으로 탐색할 후보들. node는 (상태, 행동, 비용) 튜플의 리스트. node[-1][0]은 현재 상태. node[-1][1]은 그 상태로 가기 위한 행동. node[-1][2]는 그 행동의 비용.
    frontier_states = {start} # 후보들의 상태들. set으로 저장해서 빠르게 탐색했는지 확인할 수 있게 함.
    explored = set() # 이미 탐색한 상태들. set으로 저장해서 빠르게 탐색했는지 확인할 수 있게 함.

    while frontier:
        node_index = random.randrange(len(frontier)) # 후보들 중에서 랜덤하게 하나 선택
        node = frontier.pop(node_index) # 후보에서 선택한 노드 제거
        state = node[-1][0] # 선택한 노드의 현재 상태 가져옴
        frontier_states.discard(state) # 후보에서 현재 상태 제거. discard는 set에서 값을 제거하는 함수, 값이 없어도 에러 안남.

        if problem.isGoalState(state):
            return [x[1] for x in node][1:]

        if state not in explored:
            explored.add(state)
            for successor in problem.getSuccessors(state): # 현재 상태에서 갈 수 있는 다음 상태들 가져옴. successor는 (다음 상태, 그 상태로 가기 위한 행동, 그 행동의 비용) 튜플.
                if successor[0] not in explored and successor[0] not in frontier_states:
                    parent = node[:]
                    parent.append(successor)
                    frontier.append(parent) # 후보에 다음 상태 추가
                    frontier_states.add(successor[0])

    return []


def depth_first_search(problem):
    """Search the deepest nodes in the search tree first using graph search."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    node = [(start, "", 0)]
    frontier = [node]


    raiseNotDefined() # 구현 안 했으면 프로그래밍 종료 함수


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()


def uniform_cost_search(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()


def heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem. This heuristic is trivial.
    """
    "*** YOUR CODE HERE ***"
    return 0


def aStar_search(problem, heuristic=heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()


rand = random_search
bfs = breadth_first_search
dfs = depth_first_search
astar = aStar_search
ucs = uniform_cost_search
