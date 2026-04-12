---
title: "유니티 — 게임 엔진의 세계로 첫걸음"
date: 2025-04-07 09:00:00 +0900
categories: [유니티, 입문]
tags: [Unity, 게임엔진, GameObject, 컴포넌트, C#]
---

Unity는 세계에서 가장 많이 쓰이는 게임 엔진 중 하나입니다.  
인디 게임부터 모바일 게임, VR 콘텐츠까지 — 우리가 알고 있는 수많은 게임이 Unity로 만들어졌습니다.  
이 글은 유니티를 처음 켜는 순간부터 첫 번째 씬을 구성하고 스크립트를 붙이는 것까지를 다룹니다.

---

## Unity가 하는 일

게임을 "처음부터" 만든다고 생각해 봅시다.

- 화면에 물체를 그리는 렌더링 시스템
- 물리 엔진 (중력, 충돌)
- 입력 처리 (키보드, 마우스, 터치)
- 사운드 재생
- 씬(화면) 전환
- 파일 저장/로드

이것을 전부 직접 만들면 게임 만들기 전에 지칩니다.  
**Unity가 이 모든 것을 미리 만들어서 제공합니다.** 우리는 게임 로직에만 집중하면 됩니다.

---

## 설치

1. **Unity Hub** 설치 → [unity.com/download](https://unity.com/download)
2. Unity Hub에서 **Unity Editor 설치** (LTS 버전 권장 — Long Term Support, 안정적)
3. 설치 시 모듈 선택:
   - ✅ **Visual Studio** (또는 VS Code)
   - ✅ **Windows Build Support** (Windows에서 빌드 시)
   - ✅ **Android Build Support** (모바일 목표라면)

> **LTS 버전이란?** Unity는 매년 새 버전을 냅니다. LTS는 2년간 버그 픽스를 지원하는 안정 버전입니다. 2025년 기준 **Unity 6 LTS**를 사용하세요.

---

## 유니티 인터페이스 이해

처음 유니티를 열면 여러 창이 보입니다. 하나씩 이해해 봅시다.

```
┌────────────────────────────────────────────────────────┐
│ 상단 메뉴바 (File, Edit, Assets, GameObject ...)        │
├──────────┬─────────────────────────┬───────────────────┤
│          │                         │                   │
│ Hierarchy│      Scene View         │    Inspector      │
│(씬의 목록)│   (3D 작업 공간)          │  (선택 오브젝트    │
│          │                         │   의 속성)         │
│          ├─────────────────────────┤                   │
│          │      Game View          │                   │
│          │  (실제 플레이 화면 미리보기) │                  │
├──────────┴─────────────────────────┴───────────────────┤
│                   Project Window                        │
│            (파일, 에셋, 스크립트 관리)                    │
│                   Console                              │
│              (에러, 로그 메시지)                          │
└────────────────────────────────────────────────────────┘
```

### 각 창의 역할

| 창 | 역할 |
|---|---|
| **Hierarchy** | 씬에 있는 오브젝트 목록. 여기서 오브젝트를 추가/삭제 |
| **Scene View** | 3D/2D 작업 공간. 오브젝트를 배치하는 곳 |
| **Game View** | Play 버튼을 누르면 보이는 실제 플레이 화면 |
| **Inspector** | 선택한 오브젝트의 속성과 컴포넌트 표시/편집 |
| **Project** | 프로젝트 파일 탐색기. 스크립트, 이미지, 사운드 등 |
| **Console** | 오류 메시지와 `Debug.Log()` 출력 확인 |

---

## Unity의 핵심 개념: GameObject와 Component

Unity를 이해하는 데 가장 중요한 두 개념입니다.

### GameObject — 모든 것의 기본 단위

씬에 존재하는 모든 것은 **GameObject**입니다.

- 플레이어 캐릭터 → GameObject
- 땅 → GameObject
- 카메라 → GameObject
- 빈 오브젝트 (보이지 않는 관리용) → GameObject

GameObject 자체는 **이름과 위치** 외에 아무 기능이 없습니다.

### Component — 기능 조각

기능은 **Component**를 붙여서 추가합니다.

```
[GameObject: 플레이어]
  ├── Transform          (위치, 회전, 크기 — 모든 오브젝트에 기본)
  ├── Mesh Renderer      (화면에 보이게 함)
  ├── Rigidbody          (물리 법칙 적용 — 중력, 충돌)
  ├── Collider           (충돌 영역 정의)
  └── PlayerController   (우리가 만든 스크립트)
```

이것이 Unity의 **컴포넌트 기반 아키텍처**입니다.  
레고처럼 필요한 부품을 붙였다 뗐다 합니다.

---

## 첫 번째 씬 만들기

### 1. 새 프로젝트 생성

Unity Hub → New Project → **3D Core** 선택 → 이름 입력 → Create Project

### 2. 지형 만들기

Hierarchy 창에서 우클릭 → **3D Object → Plane** 선택  
Inspector에서 이름을 "Ground"로 변경

### 3. 큐브 추가

Hierarchy → 우클릭 → **3D Object → Cube**  
Inspector에서:
- 이름: "Player"
- Position: X=0, Y=0.5, Z=0 (땅 위에 올라오도록)

### 4. 물리 추가

Player 선택 → Inspector 하단 → **Add Component** → **Rigidbody** 검색 → 추가  
이제 Play 버튼을 누르면 큐브가 중력에 따라 땅에 떨어집니다.

---

## 첫 번째 스크립트 작성

### 스크립트 생성

Project 창 → Assets 폴더 → 우클릭 → **Create → C# Script** → 이름: "PlayerController"

더블클릭하면 Visual Studio(또는 VS Code)가 열립니다.

```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    // Inspector에서 수정 가능한 공개 변수
    public float moveSpeed = 5.0f;
    public float jumpForce = 7.0f;

    // private으로 내부에서만 사용
    private Rigidbody rb;
    private bool isGrounded = false;

    // 게임 시작 시 한 번 실행
    void Start()
    {
        // GetComponent: 같은 GameObject의 컴포넌트를 가져옴
        rb = GetComponent<Rigidbody>();
        Debug.Log("PlayerController 시작!");
    }

    // 매 프레임 실행 (모니터 60fps라면 초당 60번)
    void Update()
    {
        // 입력 처리
        float h = Input.GetAxis("Horizontal");  // A/D 또는 ←/→
        float v = Input.GetAxis("Vertical");    // W/S 또는 ↑/↓

        // 이동 벡터 계산
        Vector3 move = new Vector3(h, 0f, v);

        // Translate: 현재 위치에서 이만큼 이동
        transform.Translate(move * moveSpeed * Time.deltaTime);

        // 점프 (땅에 있을 때만)
        if (Input.GetKeyDown(KeyCode.Space) && isGrounded)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
            isGrounded = false;
        }
    }

    // 충돌 시작 이벤트
    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.name == "Ground")
        {
            isGrounded = true;
        }
    }
}
```

### 스크립트 붙이기

Player GameObject를 선택 → Inspector → **Add Component** → "PlayerController" 검색 → 추가  
(또는 Project 창의 스크립트를 Hierarchy의 Player로 드래그)

### Play 버튼 → 테스트!

- WASD로 큐브가 이동합니다
- 스페이스바로 점프합니다

---

## 자주 쓰는 Unity 기초 코드

```csharp
// 위치 이동
transform.position = new Vector3(0, 1, 0);
transform.Translate(Vector3.forward * speed * Time.deltaTime);

// 오브젝트 찾기
GameObject enemy = GameObject.Find("Enemy");
GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");

// 컴포넌트 가져오기
Rigidbody rb = GetComponent<Rigidbody>();

// 오브젝트 생성 / 삭제
GameObject obj = Instantiate(prefab, position, rotation);
Destroy(obj);
Destroy(obj, 3.0f);  // 3초 후 삭제

// 로그 출력 (Console 창에서 확인)
Debug.Log("일반 메시지");
Debug.LogWarning("경고!");
Debug.LogError("에러!");
```

---

## Time.deltaTime이 왜 중요한가

```csharp
// 나쁜 방법 — 프레임 속도에 따라 이동 속도가 달라짐
transform.Translate(Vector3.forward * 5);

// 좋은 방법 — 어떤 기기에서든 초당 5미터로 통일
transform.Translate(Vector3.forward * 5 * Time.deltaTime);
```

`Time.deltaTime`은 **이전 프레임과 현재 프레임 사이의 시간(초)**입니다.  
60fps에서는 약 0.0167초, 30fps에서는 약 0.033초입니다.  
속도에 곱하면 프레임 수와 무관하게 일정한 속도를 유지합니다.

---

## 정리

- Unity는 렌더링, 물리, 입력 등 게임 제작 인프라를 제공합니다
- 씬의 모든 것은 **GameObject**이며, 기능은 **Component**로 추가합니다
- 스크립트는 `MonoBehaviour`를 상속받아 만들며, `Start()`와 `Update()`가 핵심입니다
- `Time.deltaTime`을 곱해야 프레임에 독립적인 움직임이 됩니다
- `Debug.Log()`로 Console 창에서 값을 확인하며 디버깅합니다

다음 글에서는 **Prefab과 씬 전환**을 다룹니다.  
같은 오브젝트를 여러 개 만들고, 씬 사이를 이동하는 방법을 알면 실제 게임 구조를 만들 수 있습니다.
