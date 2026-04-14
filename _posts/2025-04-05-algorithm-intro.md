---
title: "알고리즘 — 좋은 코드와 나쁜 코드를 가르는 기준"
date: 2025-04-05 09:00:00 +0900
categories: [알고리즘, 입문]
tags: [알고리즘, 시간복잡도, Big-O, 탐색, 정렬]
math: true
comments: true
---

같은 결과를 내는 두 코드가 있습니다.  
하나는 1초 만에 끝나고, 하나는 1시간이 걸립니다.  
둘 다 "동작하는 코드"이지만, 실제로 쓸 수 있는 것은 하나뿐입니다.

**알고리즘은 "얼마나 빠르고 효율적으로 문제를 푸는가"에 대한 학문입니다.**

---

## 알고리즘이란

알고리즘(Algorithm)은 **문제를 해결하는 절차 또는 방법**입니다.

라면 끓이는 방법도 알고리즘입니다.

```
1. 물 550ml를 냄비에 넣고 끓인다
2. 물이 끓으면 면과 스프, 건더기 수프를 넣는다
3. 4분 30초 더 끓인다
4. 불을 끄고 그릇에 담는다
```

이것이 알고리즘의 세 가지 조건을 만족합니다.

- **입력**: 물, 라면
- **출력**: 완성된 라면
- **유한성**: 반드시 끝납니다

코드에서 알고리즘은 "주어진 입력으로 원하는 출력을 만드는 절차"입니다.

---

## 왜 알고리즘을 공부하는가

숫자 1억 개 중에서 특정 숫자를 찾아야 한다고 가정합시다.

### 방법 1: 처음부터 하나씩 찾기 (선형 탐색)

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

최악의 경우, 숫자가 맨 마지막에 있다면 **1억 번** 비교합니다.

### 방법 2: 반씩 나눠서 찾기 (이진 탐색)

배열이 정렬되어 있다면 이렇게 할 수 있습니다.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1    # 오른쪽 절반으로 좁힘
        else:
            right = mid - 1   # 왼쪽 절반으로 좁힘

    return -1
```

1억 개에서 이진 탐색을 쓰면 최악의 경우 **약 27번**만 비교합니다.

왜냐하면 매번 절반씩 줄어들기 때문입니다.

$$1억 → 5천만 → 2500만 → ... → 1 \quad (약 27번)$$

$$\log_2(100,000,000) \approx 26.5$$

1억 번 vs 27번 — 이것이 알고리즘의 차이입니다.

---

## 시간복잡도와 Big-O 표기법

알고리즘의 속도를 비교할 때 "몇 초 걸리는가"로 따지지 않습니다.  
컴퓨터 성능마다 다르기 때문입니다.

대신 **입력 크기 n에 따라 연산 횟수가 어떻게 늘어나는가**로 따집니다.  
이를 표현하는 방법이 **Big-O 표기법**입니다.

### 대표적인 시간복잡도

| Big-O | 이름 | 예시 | n=1000일 때 |
|---|---|---|---|
| O(1) | 상수 | 배열 인덱스 접근 | 1번 |
| O(log n) | 로그 | 이진 탐색 | ~10번 |
| O(n) | 선형 | 선형 탐색, 배열 순회 | 1,000번 |
| O(n log n) | 선형로그 | 병합 정렬, 퀵 정렬 | ~10,000번 |
| O(n²) | 이차 | 버블 정렬, 이중 반복문 | 1,000,000번 |
| O(2ⁿ) | 지수 | 피보나치 재귀 | 10^301번 (사실상 불가) |

### 시각적으로 이해하기

```
연산
횟수
 ↑  O(n²)  ↗
 │         ↗
 │  O(n)  ↗ (선형)
 │       ↗
 │ O(log n) ↗ (완만)
 │          ↗
 │ O(1) ─────────
 └────────────────→ n(입력 크기)
```

### Big-O 계산 방법

```python
def example(n):
    total = 0               # O(1) — 한 번 실행

    for i in range(n):      # O(n) — n번 실행
        total += i

    for i in range(n):      # O(n²) — n×n번 실행
        for j in range(n):
            total += i * j

    return total
```

전체 시간복잡도: O(1) + O(n) + O(n²) = **O(n²)**

Big-O는 가장 큰 항만 남기고 상수는 무시합니다.  
O(3n² + 5n + 100) → **O(n²)**

---

## 직접 비교해보기: 버블 정렬 vs 병합 정렬

### 버블 정렬 — O(n²)

인접한 두 원소를 비교해서 큰 것을 뒤로 보내는 방식입니다.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):  # 이중 반복문 → O(n²)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

arr = [64, 34, 25, 12, 22, 11, 90]
bubble_sort(arr)
print(arr)   # [11, 12, 22, 25, 34, 64, 90]
```

직관적이지만 느립니다. 10만 개 정렬 시 약 100억 번 비교합니다.

### 병합 정렬 — O(n log n)

배열을 절반씩 나눠서 정렬한 뒤 합치는 방식입니다 (분할 정복).

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])   # 왼쪽 절반 재귀 정렬
    right = merge_sort(arr[mid:])   # 오른쪽 절반 재귀 정렬

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

arr = [64, 34, 25, 12, 22, 11, 90]
print(merge_sort(arr))   # [11, 12, 22, 25, 34, 64, 90]
```

10만 개 정렬 시 약 170만 번 비교합니다. 버블 정렬 대비 약 **6,000배** 빠릅니다.

---

## 공간복잡도

시간복잡도 외에 **메모리를 얼마나 쓰는가**도 중요합니다.

```python
# O(1) 공간 — 추가 메모리 거의 없음
def sum_to_n(n):
    return n * (n + 1) // 2

# O(n) 공간 — 입력 크기만큼 추가 배열 사용
def copy_array(arr):
    result = []             # 입력과 같은 크기의 배열
    for x in arr:
        result.append(x)
    return result
```

---

## 알고리즘 선택의 기준

| 상황 | 선택 |
|---|---|
| 데이터가 작다 (n < 1,000) | 간단한 알고리즘 (구현 편의 우선) |
| 데이터가 많다 (n > 100,000) | 시간복잡도 최우선 고려 |
| 정렬된 데이터 탐색 | 이진 탐색 O(log n) |
| 정렬이 필요 | 퀵 정렬 / 병합 정렬 O(n log n) |
| 메모리가 제한됨 | 공간복잡도도 고려 |

---

## 정리

- 알고리즘은 **문제를 해결하는 절차**이며, 효율성이 핵심입니다
- **시간복잡도**는 입력 크기에 따른 연산 횟수의 증가율입니다
- **Big-O 표기법**으로 알고리즘의 효율을 비교합니다
- O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) 순으로 느려집니다
- 이진 탐색은 선형 탐색보다 극적으로 빠릅니다 (1억 번 vs 27번)

다음 글에서는 **재귀(Recursion)**를 다룹니다.  
병합 정렬에서 잠깐 나온 재귀 개념 — 이것을 완전히 이해하면 많은 알고리즘 문제가 풀리기 시작합니다.
