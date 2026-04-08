# AI_HW1
# Uniform Cost Search (UCS) for 8-Puzzle

## 📌 개요

이 프로젝트는 8-퍼즐 문제를 해결하기 위해 **Uniform Cost Search (UCS)** 알고리즘을 구현한 것이다.
모든 행동의 비용이 1이지만, UCS의 **정석 구현 방식**을 따르는 것이 중요하다.

---

## ❗ 핵심 개념

### 🔥 흔한 오해

> 모든 step cost가 1이므로, 먼저 발견된 경로가 항상 최단 경로이다?

👉 **틀림**

* UCS는 **노드를 꺼낼 때(pop)** 최적성이 보장된다.
* **넣을 때(push)**는 더 좋은 경로가 나중에 발견될 수 있다.

---

## 🧠 예시

같은 상태 `S`에 대해:

* 경로 1:
  `Start → A → B → S` (cost = 3)

* 경로 2:
  `Start → C → S` (cost = 2)

👉 더 짧은 경로(cost=2)가 **나중에 발견될 수 있음**

---

## 💥 문제 상황

기존 코드에서:

```python
if successor[0] not in explored and successor[0] not in frontier_states:
```

👉 이미 frontier에 상태가 있으면 무시됨

결과:

* 더 싼 경로가 들어오지 못함
* ❗ 최적해 보장 깨짐

---

## ✅ 해결 방법

### ✔ 핵심 전략

* frontier 중복 허용
* 상태별 최소 비용 관리 (`best_cost`)
* 더 싼 경로가 나오면 갱신

---

## 🚀 Uniform Cost Search 구현

```python
def uniform_cost_search(problem):
    """Search the node of least total cost first."""

    start = problem.getStartState()

    # (cost, count, path)
    node = [(start, "", 0)]

    frontier = []
    heapq.heappush(frontier, (0, 0, node))

    explored = set()
    best_cost = {start: 0}  # 상태별 최소 비용 기록

    count = 0

    while frontier:
        cost, _, node = heapq.heappop(frontier)
        state = node[-1][0]

        # 이미 방문된 상태면 skip
        if state in explored:
            continue

        # 목표 상태 검사
        if problem.isGoalState(state):
            return [x[1] for x in node][1:]

        explored.add(state)

        for successor, action, stepCost in problem.getSuccessors(state):
            new_cost = cost + stepCost

            # 더 싼 경로일 때만 갱신
            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost

                new_node = node[:]
                new_node.append((successor, action, stepCost))

                heapq.heappush(frontier, (new_cost, count, new_node))
                count += 1

    return []
```

---

## 🔍 기존 코드 vs 개선 코드

| 항목          | 기존 코드     | 개선 코드          |
| ----------- | --------- | -------------- |
| frontier 중복 | ❌ 막음      | ✔ 허용           |
| 비용 비교       | ❌ 없음      | ✔ best_cost 사용 |
| 비용 계산       | ❌ 전체 재계산  | ✔ 누적           |
| 최적성 보장      | ❌ 깨질 수 있음 | ✔ 보장           |

---

## 🧠 핵심 포인트

### 1️⃣ frontier 중복 허용

같은 상태라도 여러 번 들어갈 수 있음
→ 더 싼 경로가 살아남는다

---

### 2️⃣ best_cost 사용

```python
best_cost[state] = 최소 비용
```

→ UCS의 핵심

---

### 3️⃣ explored 처리 타이밍

```python
if state in explored:
    continue
```

→ pop 이후 처리해야 함

---

## ⚖️ BFS vs UCS

| 알고리즘 | 기준         |
| ---- | ---------- |
| BFS  | depth (깊이) |
| UCS  | cost (비용)  |

👉 cost가 모두 1이어도
**구조적으로 BFS와 완전히 동일하지는 않다**

---

## ✅ 결론

> UCS는 "한 번 방문한 상태를 막는 알고리즘"이 아니라
> **"더 싼 경로가 나오면 계속 갱신하는 알고리즘"이다.**

---

## 🚀 한 줄 요약

👉 **모든 비용이 1이어도, 더 짧은 경로가 나중에 발견될 수 있으므로 중복을 허용해야 한다.**

---
