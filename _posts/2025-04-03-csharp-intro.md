---
title: "C# — .NET 위에서 달리는 현대적 언어"
date: 2025-04-03 09:00:00 +0900
categories: [C#, 입문]
tags: [C#, dotNET, Unity, 객체지향, 기초문법]
comments: true
---

C#(씨샵)은 2000년 Microsoft가 만든 언어입니다.  
설계 목표는 명확했습니다 — **C++의 강력함과 Java의 안전함을 동시에 갖는 것**.  
그리고 지금 우리가 C#을 배워야 하는 이유는 하나 더 있습니다. **Unity가 C#을 사용하기 때문입니다.**

---

## C#은 어디에 쓰이는가

- 🎮 **게임 개발** — Unity 엔진의 공식 스크립팅 언어
- 🖥️ **Windows 앱** — WPF, WinUI를 통한 데스크톱 앱
- 🌐 **웹 백엔드** — ASP.NET Core로 서버 개발
- ☁️ **클라우드** — Azure와의 긴밀한 통합

이 중 게임 개발자를 목표로 한다면 C#은 사실상 필수 언어입니다.

---

## .NET이란 무엇인가

C# 코드는 직접 기계어로 번역되지 않습니다.  
대신 **CLR(Common Language Runtime)**이라는 가상 환경 위에서 실행됩니다.

```
C# 소스코드
     ↓ 컴파일 (csc)
IL 코드 (중간 언어, .dll / .exe)
     ↓ JIT 컴파일 (실행 시)
기계어 (CPU가 실행)
```

이 덕분에 메모리 관리를 C/C++처럼 직접 하지 않아도 됩니다.  
**가비지 컬렉터(GC)**가 사용이 끝난 메모리를 자동으로 정리합니다.

| | C++ | C# |
|---|---|---|
| 메모리 관리 | 개발자 직접 | GC 자동 처리 |
| 실행 환경 | 바로 기계어 | .NET CLR 위 |
| 속도 | 매우 빠름 | 빠름 (JIT 최적화) |
| 안전성 | 낮음 (직접 관리) | 높음 (GC 보호) |

---

## 개발 환경 설치

1. [dotnet.microsoft.com](https://dotnet.microsoft.com) 에서 **.NET SDK** 설치
2. VS Code + **C# Dev Kit** 확장 설치  
   (또는 Visual Studio Community — Windows에서 가장 편합니다)

설치 확인:

```bash
dotnet --version
# 출력 예: 8.0.100
```

---

## Hello, World! in C#

```csharp
using System;

class Program {
    static void Main(string[] args) {
        Console.WriteLine("Hello, World!");
    }
}
```

C++과 비교하면 구조가 비슷해 보이지만 차이가 있습니다.

| | C++ | C# |
|---|---|---|
| 출력 | `cout << "Hello"` | `Console.WriteLine("Hello")` |
| 헤더/네임스페이스 | `#include <iostream>` | `using System;` |
| 진입점 | `int main()` | `static void Main()` |

### Top-level statements (.NET 6+)

최신 C#에서는 `class`와 `Main` 없이 바로 코드를 작성할 수 있습니다.

```csharp
Console.WriteLine("Hello, World!");
```

Unity 스크립트에서는 이 방식을 쓰지 않지만, 콘솔 프로그램을 빠르게 테스트할 때 편합니다.

---

## 기본 자료형

```csharp
int    age     = 25;          // 32비트 정수
long   bigNum  = 9999999999L; // 64비트 정수
double pi      = 3.14159;     // 64비트 실수
float  small   = 3.14f;       // 32비트 실수
bool   isAlive = true;        // 참/거짓
char   letter  = 'A';         // 문자 하나
string name    = "철수";       // 문자열 (C#에서 string은 기본 타입)
```

C#에서 `string`은 소문자로 씁니다. 이것은 `System.String`의 별칭입니다.

### var — 타입 추론

```csharp
var score = 95;         // int로 추론
var name  = "영희";      // string으로 추론
var pi    = 3.14;       // double로 추론
```

`var`를 쓰면 컴파일러가 오른쪽 값을 보고 타입을 자동으로 정합니다.  
타입이 길고 복잡할 때 코드가 깔끔해집니다. 단, **우변을 보면 타입이 분명한 경우에만** 쓰는 것이 좋습니다.

---

## 조건문과 반복문

C, C++과 문법이 거의 동일합니다.

```csharp
using System;

class Program {
    static void Main() {
        int score = 87;

        // if-else
        if (score >= 90) {
            Console.WriteLine("A");
        } else if (score >= 80) {
            Console.WriteLine("B");
        } else {
            Console.WriteLine("C 이하");
        }

        // for 반복문
        for (int i = 1; i <= 5; i++) {
            Console.Write(i + " ");
        }
        Console.WriteLine();   // 줄바꿈

        // foreach — C#이 C++보다 편리한 부분
        int[] numbers = { 10, 20, 30, 40, 50 };
        foreach (int n in numbers) {
            Console.Write(n + " ");
        }
    }
}
```

```
B
1 2 3 4 5
10 20 30 40 50
```

`foreach`는 배열이나 컬렉션을 순회할 때 C++보다 훨씬 간결합니다.

---

## 클래스 (C# 스타일)

C#의 클래스는 C++보다 문법이 더 명확하고 현대적입니다.

```csharp
using System;

class Player {
    // 프로퍼티 (Property) — C#만의 강력한 기능
    public string Name  { get; set; }
    public int    HP    { get; private set; }   // 외부에서 읽기만 가능
    public int    MaxHP { get; }

    // 생성자
    public Player(string name, int maxHP) {
        Name  = name;
        MaxHP = maxHP;
        HP    = maxHP;
    }

    // 메서드
    public void TakeDamage(int damage) {
        HP -= damage;
        if (HP < 0) HP = 0;
        Console.WriteLine($"{Name}이(가) {damage}의 데미지를 받았습니다. (HP: {HP}/{MaxHP})");
    }

    public void Heal(int amount) {
        HP += amount;
        if (HP > MaxHP) HP = MaxHP;
        Console.WriteLine($"{Name}이(가) {amount} 회복했습니다. (HP: {HP}/{MaxHP})");
    }

    public bool IsAlive() {
        return HP > 0;
    }
}

class Program {
    static void Main() {
        Player hero = new Player("기사", 100);

        hero.TakeDamage(35);
        hero.TakeDamage(50);
        hero.Heal(20);

        Console.WriteLine($"{hero.Name} 생존 여부: {hero.IsAlive()}");
    }
}
```

```
기사이(가) 35의 데미지를 받았습니다. (HP: 65/100)
기사이(가) 50의 데미지를 받았습니다. (HP: 15/100)
기사이(가) 20 회복했습니다. (HP: 35/100)
기사 생존 여부: True
```

### 프로퍼티란?

C#에서 `{ get; set; }`은 **프로퍼티**입니다. 멤버 변수처럼 사용하지만, 내부적으로 get/set 메서드가 자동 생성됩니다.

```csharp
// 이것과:
public int HP { get; private set; }

// 이것이 같습니다 (컴파일러가 자동 생성):
private int _hp;
public int HP {
    get { return _hp; }
    private set { _hp = value; }
}
```

`HP`를 외부에서 읽는 것(`get`)은 허용하지만, 바꾸는 것(`set`)은 클래스 내부에서만 허용합니다.

### 문자열 보간 ($"...")

C#의 편리한 기능입니다.

```csharp
string name = "철수";
int age = 20;

// 기존 방식
Console.WriteLine("이름: " + name + ", 나이: " + age);

// 문자열 보간 — 훨씬 읽기 쉽습니다
Console.WriteLine($"이름: {name}, 나이: {age}");
```

---

## C#이 Unity에서 어떻게 쓰이나

Unity에서 C# 스크립트는 이런 형태입니다.

```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour {
    public float moveSpeed = 5.0f;

    // 게임 시작 시 한 번 실행
    void Start() {
        Debug.Log("플레이어 준비 완료");
    }

    // 매 프레임마다 실행
    void Update() {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        Vector3 move = new Vector3(h, 0, v);
        transform.Translate(move * moveSpeed * Time.deltaTime);
    }
}
```

`MonoBehaviour`를 상속받고, `Start()`와 `Update()`를 오버라이드하는 구조입니다.  
지금은 형태만 눈에 익혀두세요. 유니티 편에서 자세히 다룹니다.

---

## 정리

- C#은 .NET 위에서 동작하며, GC가 메모리를 자동 관리합니다
- Unity의 스크립팅 언어이므로 게임 개발자에게 필수입니다
- **프로퍼티**(`{ get; set; }`)는 C#만의 강력한 캡슐화 도구입니다
- **문자열 보간**(`$"..."`)으로 코드가 훨씬 읽기 쉬워집니다
- `foreach`로 컬렉션을 쉽게 순회할 수 있습니다

다음 글에서는 **상속과 인터페이스**를 다루겠습니다.  
Unity에서 컴포넌트를 설계하는 방식이 바로 이 개념에서 나옵니다.
