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
    
# 시작상태반환, 
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
    node = [(start, "", 0)] # 노드 초기화. 노드는 (상태, 행동, 비용) 튜플의 리스트. 처음에는 시작 상태만 포함. 행동은 빈 문자열, 비용은 0으로 초기화. 경로들의 리스트 [[(state1, action, cost), ...],[(state2, action, cost), ...]]
    frontier = [node]# 앞으로 탐색할 후보들. node는 (상태, 행동, 비용) 튜플의 리스트. node[-1][0]은 현재 상태. node[-1][1]은 그 상태로 가기 위한 행동. node[-1][2]는 그 행동의 비용.
    frontier_states = {start} # 후보들의 상태들. set으로 저장해서 빠르게 탐색했는지 확인할 수 있게 함.
    explored = set() # 이미 탐색한 상태들. set으로 저장해서 빠르게 탐색했는지 확인할 수 있게 함.

    while frontier:
        node_index = random.randrange(len(frontier)) # 후보들 중에서 랜덤하게 하나 선택
        node = frontier.pop(node_index) # 후보에서 선택한 노드 제거
        state = node[-1][0] # 선택한 노드의 현재 상태 가져옴 
        frontier_states.discard(state) # 후보에서 현재 상태 제거. discard는 set에서 값을 제거하는 함수, 값이 없어도 에러 안남.

        if problem.isGoalState(state): # 현재 상태가 목표 상태인지 확인
            return [x[1] for x in node][1:]

        if state not in explored: # 현재 상태가 아직 탐색되지 않았다면
            explored.add(state) # 현재 상태를 탐색한 상태 집합에 추가
            for successor in problem.getSuccessors(state): # 현재 상태에서 갈 수 있는 다음 상태들 가져옴. successor는 (다음 상태, 그 상태로 가기 위한 행동, 그 행동의 비용) 튜플.
                if successor[0] not in explored and successor[0] not in frontier_states: # 다음 상태가 아직 탐색되지 않았고 후보에도 없다면
                    parent = node[:] # 현재 노드의 경로를 복사해서 다음 노드의 경로로 사용. node는 (상태, 행동, 비용) 튜플의 리스트. node[-1]이 현재 상태, 행동, 비용. successor는 (다음 상태, 그 상태로 가기 위한 행동, 그 행동의 비용) 튜플. successor[0]은 다음 상태, successor[1]은 그 상태로 가기 위한 행동, successor[2]는 그 행동의 비용.
                    parent.append(successor) # 다음 노드의 경로에 다음 상태, 행동, 비용 추가. parent는 (상태, 행동, 비용) 튜플의 리스트. parent[-1]이 다음 상태, 행동, 비용.
                    frontier.append(parent) # 후보에 다음 상태 추가 
                    frontier_states.add(successor[0])

    return []


def depth_first_search(problem):
    """Search the deepest nodes in the search tree first using graph search."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState() 
    node = [(start, "", 0)] 
    frontier = [node]
    frontier_states = {start} # 상태 리스트 ex) 123456780
    explored = set() 
    
    while frontier:
        node = frontier.pop() # 후보에서 가장 마지막 노드 제거 (깊이 우선 탐색이므로)
        state = node[-1][0] # 선택한 노드의 현재 상태 가져옴
        frontier_states.discard(state)  # 후보에서 현재 상태 제거

        if problem.isGoalState(state): # 현재 상태가 목표 상태인지 확인
            return [x[1] for x in node][1:] #  목적지까지의 행동 리스트 반환. node는 (상태, 행동, 비용) 튜플의 리스트. node[0]은 시작 상태, 행동은 빈 문자열, 비용은 0. node[1]부터는 실제 행동과 비용이 들어있음. [x[1] for x in node][1:]는 node에서 행동 부분만 추출해서 리스트로 만들고, 첫 번째 요소(시작 상태의 행동)를 제외한 나머지를 반환.   
        
        if state not in explored: # 현재 상태가 아직 탐색되지 않았다면
            explored.add(state) # 현재 상태를 탐색한 상태 집합에 추가
            for successor in problem.getSuccessors(state): # 현재 상태에서 갈 수 있는 다음 상태들 가져옴. successor는 (다음 상태, 그 상태로 가기 위한 행동, 그 행동의 비용) 튜플.
                 if successor[0] not in explored and successor[0] not in frontier_states:# 다음 상태가 아직 탐색되지 않았고 후보에도 없다면
                    parent = node[:] #     현재 노드의 경로를 복사해서 다음 노드의 경로로 사용. node는 (상태, 행동, 비용) 튜플의 리스트. node[-1]이 현재 상태, 행동, 비용. successor는 (다음 상태, 그 상태로 가기 위한 행동, 그 행동의 비용) 튜플. successor[0]은 다음 상태, successor[1]은 그 상태로 가기 위한 행동, successor[2]는 그 행동의 비용.
                    parent.append(successor) # 다음 노드의 경로에 다음 상태, 행동, 비용 추가. parent는 (상태, 행동, 비용) 튜플의 리스트. parent[-1]이 다음 상태, 행동, 비용.
                    frontier.append(parent) # 후보에 다음 상태 추가
                    frontier_states.add(successor[0])# 후보 상태 집합에도 다음 상태 추가

    return []



def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
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

#getSuccessors 현재 상태에서 갈 수 있는 다음 상태들 가져옴. successor는 (다음 상태, 그 상태로 가기 위한 행동, 그 행동의 비용) 튜플. successor[0]은 다음 상태, successor[1]은 그 상태로 가기 위한 행동, successor[2]는 그 행동의 비용.
def uniform_cost_search(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

# 각 노드는 현재상태(state), 부모 노드(parent), 수행된 행동(action), 경로비용(cost)으로 표현. node는 (상태, 행동, 비용) 튜플의 리스트. node[-1]이 현재 상태, 행동, 비용. node[0]은 시작 상태, 행동은 빈 문자열, 비용은 0. node[1]부터는 실제 행동과 비용이 들어있음. frontier는 우선순위 큐로 구현. frontier_states는 후보들의 상태 집합으로 빠르게 탐색했는지 확인할 수 있게 함. explored는 이미 탐색한 상태 집합으로 빠르게 탐색했는지 확인할 수 있게 함. 우선순위 큐에 노드를 추가할 때는 그 노드까지의 총 경로비용을 기준으로 함. 
# 1. 초기 상태를 frontier에 삽입
# 2. frontier에서 경로 비용이 가장 작은 노드 선택
# 3. 해당 노드가 목표 상태인지 검사, 
# 4. 목표 상태이면 탐색 종료, 아니면 자식 노드 생성
# 5. 각 자식 노드의 경로 비용 계산 후 frontier에 삽입, frontier가 비어 있을 때까지 탐색 반복.
# 모든 간선 비용이 동일한 경우 BFS와 동일한 구조로 동작
# 중복체크? 현재 상태가 이미 탐색된 상태인지 확인해야하나?

    start = problem.getStartState() 
    node = [(start, "", 0)] 
    frontier = []
    heapq.heappush(frontier, (0, 0, node)) # 비용이 가장 낮은 노드가 먼저 나오도록 우선순위 큐에 추가. (비용, 노드) 튜플로 저장.
   # 현재 상태의 비용보다 작은 비용이 frontier에 있는지 확인하고 있으면 frontier에 노드를 넣으면 안됨. 
    # fontier에 넣은 상태를 map으로 관리. key: 상태, value: 그 상태까지의 비용. 이 map에 있는 value가 현재 frontier에 넣으려는 노드보다 작을경우 넣지 않기, 
    # 어차피 explored에 들어가면 이미 탐색된 상태이므로 frintier에 넣지 않음. '
    # 파이썬에선 dict가 map역할. 
    # 파이썬에서 언패킹 할때 정보 버리기: _로 받음. 
    frontier_states = {start: 0}
    explored = set() 
    count = 0 # while 문 안에서 count = 0을 하게 되면 다른 상태에서 파생된 두 상태를 비교할때 서로 같은길이일 경우 우선순위를 비교못함. 

    while frontier:
        cost, _, node = heapq.heappop(frontier) # 후보에서 비용이 가장 낮은 노드 제거. 
        state = node[-1][0] 

        # pop 된 순간 그 노드로 가는 경로의 최적해임.
        
        if problem.isGoalState(state): 
            return [x[1] for x in node][1:]
        
        if state not in explored: 
            explored.add(state) # 현재 상태를 탐색한 상태 집합에 추가
            for successor in problem.getSuccessors(state):
                if successor[0] not in explored and successor[0] in frontier_states and frontier_states[successor[0]] > cost + successor[2]: # 다음 상태가 아직 탐색되지 않았고 후보에도 없다면:
                    parent = node[:]
                    parent.append(successor)
                    # 매번 길이를 다시 구할 필요 없음 oldcost+ 1하면 됨. 
                    heapq.heappush(frontier, (problem.getCostOfActions([x[1] for x in parent][1:]), count, parent)) # 다음 노드를 우선순위 큐에 추가. 비용은 현재 노드까지의 행동 리스트의 총 비용으로 계산. [x[1] for x in parent][1:]는 parent에서 행동 부분만 추출해서 리스트로 만들고, 첫 번째 요소(시작 상태의 행동)를 제외한 나머지를 반환. problem.getCostOfActions(...)는 그 행동 리스트의 총 비용을 계산.
                    frontier_states[successor[0]] = cost + successor[2]
                    count += 1

        

    return []


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
