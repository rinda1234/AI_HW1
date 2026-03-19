# HW1: 8-Puzzle Solver

이 프로젝트는 8-Puzzle 문제를 여러 탐색 알고리즘으로 해결하고, 결과를 비교 분석해야하는 과제를 위해 제공됩니다.

## 파일 구성

| 파일명 | 설명 |
|---|---|
| `eightpuzzle.py` | 8-Puzzle 문제 정의 |
| `search.py` | 학생이 구현하고 제출할 파일 |
| `main.py` | 콘솔 실행 파일 |
| `main_ui.py` | 브라우저 기반 시각화 실행 파일 |
| `00. instruction.html` | 브라우저용 과제 안내문 |
| `00. instruction.pdf` | 배포용 PDF 안내문 |
| `01. report_template.docx` | 학생 제출용 보고서 템플릿 |
| `requirements.txt` | 실행 환경 안내 |

## 먼저 읽을 문서

- 브라우저에서 보기 좋은 안내문: `00. instruction.html`
- PDF 안내문: `00. instruction.pdf`
- 배포된 `search.py`는 과제 템플릿이므로, 알고리즘 구현 이전에는 실행 파일이 완전히 동작하지 않을 수 있습니다.

## 실행 방법

### 콘솔 실행

```bash
python3 main.py
```

### UI 실행

```bash
python3 main_ui.py
```

브라우저 기반 GUI에서 실행되어야 합니다. 브라우저가 자동으로 열리지 않으면 아래 주소로 접속해야 합니다.

```text
http://127.0.0.1:8000
```

브라우저 기반 GUI 사용 방법:

1. `New Puzzle` 버튼을 눌러 랜덤 퍼즐을 생성합니다.
2. 알고리즘 버튼(`DFS`, `BFS`, `UCS`, `A*`, `Random`) 중 하나를 선택합니다.
3. 해결 과정이 애니메이션으로 표시됩니다.
4. `Stop` 버튼으로 애니메이션을 멈추고, `Reset` 버튼으로 초기 상태로 돌아갈 수 있습니다.

## 과제 수행 파일

- 학생은 반드시 `search.py`를 수정하여 제출해야 합니다. (제출파일명: `[분반]_[이름]_[학번]_search.py`)
- 학생이 **수정 가능한 파일은 `search.py` 하나뿐**입니다.
- `eightpuzzle.py`, `main.py`, `main_ui.py`, 안내문/템플릿 파일은 모두 읽기 전용으로 사용해야 합니다.
- 보고서 작성 시에도 `search.py`를 기준으로 알고리즘을 분석해야 합니다.

## 제출 방식 (ZIP)

- 최종 제출은 **ZIP 파일 1개**로 해야 합니다.
- ZIP 안에는 아래 2개 파일이 모두 들어 있어야합니다.
  - `search.py`
  - 보고서 PDF (`[분반]_[이름]_[학번]_report.pdf` 권장)
- ZIP 파일명 권장 형식:
  - `[분반]_[이름]_[학번]_hw1.zip`

## 구현해야 할 알고리즘

학생은 `search.py`에서 다음 알고리즘들을 구현해야 합니다.

1. `DFS (Depth-First Search)`
   - 가장 깊은 노드부터 탐색
   - 그래프 탐색 방식으로 구현
   - 최적 해를 보장하지 않음

2. `BFS (Breadth-First Search)`
   - 가장 얕은 노드부터 탐색
   - 모든 간선 비용이 동일할 때 최단 경로 보장

3. `UCS (Uniform Cost Search)`
   - 누적 비용이 가장 낮은 노드부터 탐색
   - 비용 기준 최적 해 보장

4. `A* Search`
   - 경로 비용과 휴리스틱을 함께 고려한 탐색
   - 적절한 `heuristic()` 함수 구현 필요
   - 예: Manhattan distance

## 참고 사항

- Graph search로 구현해야 합니다. 이미 방문한 상태를 다시 반복 탐색하지 않도록 해야 합니다.
- 각 알고리즘은 목표 상태에 도달하기 위한 `action` 리스트를 반환해야 합니다.
- 가능한 action은 `up`, `down`, `left`, `right`입니다.

## 비교 분석 권장 알고리즘

- BFS
- UCS
- A*

DFS와 Random Search는 함께 다루되, 한계와 주의점을 분석하는 방향으로 접근해야 합니다.
