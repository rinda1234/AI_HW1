from eightpuzzle import createRandomEightPuzzle, EightPuzzleSearchProblem
from search import rand, bfs, dfs, astar, ucs

if __name__ == '__main__': # 이 파일을 직접 실행했을 때만 아래 코드 실행. 다른 파일에서 import 해도 실행 안됨. 
    puzzle = createRandomEightPuzzle(50) # 목표 상태에서 5번 움직여 섞은 퍼즐을 만듦
    print('A random puzzle:') # 생성된 퍼즐 상태 출력
    print(puzzle)

    problem = EightPuzzleSearchProblem(puzzle) # 이 문제를 탐색 알고리즘일 다룰 수 있게 탐색 문제 객체로 바꿈.
    search_algorithms = [dfs] # 사용할 알고리즘 목록, 다른 알고리즘도 같이 넣어두면 순차적으로 실행
    for alg in search_algorithms:
        path = alg(problem) # 해당 알고리즘으로 퍼즐을 풂. 반환되는 path는 ['up', 'left', 'down'] 보통 이런 식의 이동 명령 리스트
        print(f'{alg.__name__} found a path of {len(path)} moves: ') # 알고리즘 이름, 이동 횟수, 실제 이동 목록 moves: {str(path)}
 
        
        curr = puzzle # 현재 상태를 초기 퍼즐로 시
        for i, p in enumerate(path, 1): # 각 이동을 실제로 하나씩 적용해보면서 출력. path에 들어있는 이동을 하나씩 꺼냄, i: 1부터 시작하는 인덱스, p: 이동 명령 (up, down, left, right)
            curr = curr.result(p) # 현재 퍼즐에 이동 p를 적용해서 다음 상태로 갱신
            #print(f'After {i} move{("", "s")[i > 1]}: {p}') # 이동횟수와 방향 출력.

    search_algorithms = [bfs, ucs, astar] # 사용할 알고리즘 목록, 다른 알고리즘도 같이 넣어두면 순차적으로 실행
    for alg in search_algorithms:
        path = alg(problem) # 해당 알고리즘으로 퍼즐을 풂. 반환되는 path는 ['up', 'left', 'down'] 보통 이런 식의 이동 명령 리스트
        print(f'{alg.__name__} found a path of {len(path)} moves: {str(path)}') # 알고리즘 이름, 이동 횟수, 실제 이동 목록 
 
        
        curr = puzzle # 현재 상태를 초기 퍼즐로 시작
        for i, p in enumerate(path, 1): # 각 이동을 실제로 하나씩 적용해보면서 출력. path에 들어있는 이동을 하나씩 꺼냄, i: 1부터 시작하는 인덱스, p: 이동 명령 (up, down, left, right)
            curr = curr.result(p) # 현재 퍼즐에 이동 p를 적용해서 다음 상태로 갱신
            #print(f'After {i} move{("", "s")[i > 1]}: {p}') # 이동횟수와 방향 출력.
