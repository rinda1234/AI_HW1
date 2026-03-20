import random

from search import SearchProblem

# 현재 퍼즐 상태 하나를 나타내는 클래스
class EightPuzzleState:
    """
    This class defines the mechanics of the puzzle itself.
    The task of recasting this puzzle as a search problem is left to the EightPuzzleSearchProblem class.
    """
# 퍼즐 상태를 처음 만드는 생성자, numbers는 길이 9짜리 리스트이고 0~8 숫자가 들어있음. 
    def __init__(self, numbers): # 멤버변수는 여기서 정의되어야함. 밖에서 정의된거는 정적변수처럼 쓰는 듯.
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blanㅎk
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = [] #2차원 배열로 퍼즐 저장 
        numbers = numbers[:] #원본 리스트 복사
        numbers.reverse() # 뒤집은 다음 pop()으로 앞에서 부터 꺼낸 것처럼 쓰려고, pop()은 제일 뒤 원소부터 꺼냄. 
        for row in range(3):
            self.cells.append([])
            for col in range(3):
                self.cells[row].append(numbers.pop()) # 한행씩 채움. 
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col #0이 있는 위치를 blankLocation에 저장
    # 현재 퍼즐이 목표상태에 있는지 확인하는 함수. 
    def isGoal(self): # 클래스 매서드에 self 가 들어가는 이유는 파이썬 클래스 매서드는 그 객체 자신을 같이 받아야 하기 때문에.
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            | 1 | 2 | 3 |
            -------------
            | 4 | 5 | 6 |
            -------------
            | 7 | 8 | 0 |
            -------------
# 현재 목표 항태
        >>> EightPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """ 
        # 퍼즐판 순서대로 검사.
        current = 1
        for row in range(3):
            for col in range(3):
                if current % 9 != self.cells[row][col]:
                    return False
                current += 1
        return True
# 현재 빈칸에서 어떤 방향으로 움직일 수 있는지 반환하는 함수..
    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0]).legalMoves()
        ['up', 'left']
        """
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if row != 2:
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 2:
            moves.append('right')
        return moves
# 현재상태에서 move를 적용했을때의 새로운 퍼즐 상태, 새객체를 반환함. 
    def result(self, move):
        """
        Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.
        Instead, it returns a new object.
        """
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise Exception("Illegal Move")
        # 빈퍼즐판을 하나 만들고 현재 퍼즐판을 깊은복사해서 넣음. 
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # 현재 빈칸위치와 이동할 위치의 숫자를 서로 바꿈. 
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle
# 두퍼즐 상태가 같은지 비교하는 함수
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range(3):
            if self.cells[row] != other.cells[row]: # 각 행이 전부 같으면 같은 상태로 판단 
                return False
        return True
# 상태릃 set이나 dict의 key로 쓰기 위해 필요. 탐색에서 방문한 상태를 저장할때 사용.set: 값자체만 저장(방문했는지 체크), dict: 값과 key를 저장.
    def __hash__(self):
        return hash(str(self.cells))
# 퍼즐을 예쁘게 출력하기 위한 함수. 
    def __str__(self):
        lines = []
        horizontal_line = ('-' * 13)
        lines.append(horizontal_line)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontal_line)
        return '\n'.join(lines)

# 이클래스는 탐색 문제로서의 정의를 담고있음. 
class EightPuzzleSearchProblem(SearchProblem):
    """
      Implementation of a SearchProblem for the EightPuzzle domain
      Each state is represented by an instance of an eightPuzzle.
    """
# 초기 퍼즐상태를 저장.
    def __init__(self, puzzle):
        self.puzzle = puzzle
# 탐색 시작 상태를 반환, 처음 퍼즐판을 넘겨줌. 
    def getStartState(self):
        return self.puzzle
# 주어진 상태가 목표인지 검사
    def isGoalState(self, state):
        return state.isGoal()
# 현재 상태에서 갈 수 있는 다음 상태들 전부 반환, 예를 들어 가능한 이동이 ['up', 'left']면 up 했을때와 left 했을때 새 상태를 각각 만들어 저장함. 
    def getSuccessors(self, state): # type: ignore
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ
# 행동 리스트 전체 비용을 계산. 모든 행동비용이 1이므로, 총비용 = 행동 개수.
    def getCostOfActions(self, actions): # type: ignore
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves
        """
        return len(actions)

# 랜덤한 퍼즐을 생성하는 함수
def createRandomEightPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying a series of 'moves' random moves to a solved puzzle.
    """
    puzzle = EightPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0])
    for _ in range(moves):
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle
