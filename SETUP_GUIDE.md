# 📋 GitHub Pages + Giscus 댓글 완전 설치 가이드

## 파일 구조 전체

```
username.github.io/
├── _config.yml                      ← 블로그 전체 설정
├── assets/
│   └── css/
│       └── custom-theme.scss        ← 커스텀 다크 테마
└── _posts/
    ├── 2025-04-01-c-language-intro.md
    ├── 2025-04-02-cpp-intro.md
    ├── 2025-04-03-csharp-intro.md
    ├── 2025-04-04-computer-science-intro.md
    ├── 2025-04-05-algorithm-intro.md
    ├── 2025-04-06-game-design-intro.md
    └── 2025-04-07-unity-intro.md
```

---

## STEP 1. Chirpy 테마 저장소 fork

1. GitHub에 로그인합니다
2. 아래 주소로 이동합니다:
   ```
   https://github.com/cotes2333/chirpy-starter
   ```
3. 오른쪽 상단 **Fork** 버튼 클릭
4. Repository name을 반드시 이렇게 입력합니다:
   ```
   username.github.io
   ```
   ⚠️ `username`은 본인 GitHub 아이디로 바꿔야 합니다.
5. **Create fork** 클릭

---

## STEP 2. GitHub Pages 활성화

1. Fork된 저장소 → **Settings** 탭 클릭
2. 왼쪽 메뉴 → **Pages** 클릭
3. **Build and deployment** 섹션에서:
   - Source: **GitHub Actions** 선택
4. 저장합니다

이제 push할 때마다 자동으로 빌드 및 배포됩니다.

---

## STEP 3. 저장소 로컬에 clone

```bash
git clone https://github.com/username/username.github.io.git
cd username.github.io
```

---

## STEP 4. 파일 배치

제공된 파일들을 아래와 같이 복사합니다.

```bash
# _config.yml 교체
cp path/to/_config.yml ./_config.yml

# 커스텀 테마 CSS 추가
mkdir -p assets/css
cp path/to/custom-theme.scss ./assets/css/custom-theme.scss

# 포스트 파일 추가
mkdir -p _posts
cp path/to/_posts/*.md ./_posts/
```

---

## STEP 5. _config.yml 수정

`_config.yml`을 열고 아래 항목을 본인 정보로 수정합니다.

```yaml
url: "https://YOUR_GITHUB_USERNAME.github.io"   # ← 변경
github:
  username: YOUR_GITHUB_USERNAME                 # ← 변경
social:
  name: Your Name                                # ← 변경
  email: your@email.com                          # ← 변경
```

커스텀 CSS가 로드되도록 `_config.yml`에 아래 항목도 추가합니다.

```yaml
# _config.yml 하단에 추가
head_scripts:
  - /assets/css/custom-theme.scss
```

또는 Chirpy 테마에서는 `_includes/head.html`에 직접 추가하는 방법도 있습니다:

```html
<!-- _includes/head.html 의 </head> 직전에 추가 -->
<link rel="stylesheet" href="{{ '/assets/css/custom-theme.css' | relative_url }}">
```

---

## STEP 6. Giscus 댓글 설정

### 6-1. 저장소 Discussions 활성화

1. 저장소 → **Settings** → **Features**
2. **Discussions** 체크박스 활성화

### 6-2. Giscus GitHub App 설치

1. 아래 주소로 이동합니다:
   ```
   https://github.com/apps/giscus
   ```
2. **Install** 클릭
3. **Only select repositories** 선택
4. `username.github.io` 저장소 선택
5. **Install** 클릭

### 6-3. repo_id와 category_id 발급

1. 아래 주소로 이동합니다:
   ```
   https://giscus.app/ko
   ```
2. **저장소** 입력란에 입력:
   ```
   username/username.github.io
   ```
3. "성공" 메시지가 나오면 아래로 스크롤
4. **Discussion 카테고리** → **Comments** 선택
5. **페이지 ↔ discussion 매핑** → **pathname** 선택
6. 아래 생성된 설정에서 값을 복사합니다:

```html
<script src="https://giscus.app/client.js"
        data-repo="username/username.github.io"
        data-repo-id="R_xxxxxxxxxx"       ← 이것이 repo_id
        data-category="Comments"
        data-category-id="DIC_xxxxxxxxxx" ← 이것이 category_id
        ...>
</script>
```

### 6-4. _config.yml에 붙여넣기

```yaml
comments:
  active: giscus
  giscus:
    repo: username/username.github.io
    repo_id: "R_xxxxxxxxxx"        # ← 위에서 복사한 값
    category: Comments
    category_id: "DIC_xxxxxxxxxx"  # ← 위에서 복사한 값
    mapping: pathname
    input_position: bottom
    lang: ko
    reactions_enabled: "1"
```

---

## STEP 7. push하여 배포

```bash
git add .
git commit -m "블로그 초기 설정 및 포스트 추가"
git push origin main
```

push 후 약 2~3분 뒤 아래 주소에서 확인합니다:
```
https://username.github.io
```

---

## STEP 8. 로컬에서 미리보기 (선택)

배포 전에 로컬에서 먼저 확인하고 싶다면 Ruby와 Jekyll을 설치합니다.

**macOS:**
```bash
brew install ruby
gem install bundler
bundle install
bundle exec jekyll serve
```

**Windows:**
- [RubyInstaller](https://rubyinstaller.org/) 설치 (DEVKIT 포함 버전)
- 명령 프롬프트에서:
```bash
gem install bundler
bundle install
bundle exec jekyll serve
```

브라우저에서 `http://localhost:4000` 접속하면 미리보기가 됩니다.

---

## 앞으로 글 작성하는 방법

### 파일명 규칙

```
_posts/YYYY-MM-DD-영문-제목-하이픈.md
```

예: `_posts/2025-04-15-c-pointer-intro.md`

### 파일 상단 (Front Matter) 형식

```yaml
---
title: "포인터 — C언어의 꽃이자 공포"
date: 2025-04-15 09:00:00 +0900
categories: [C언어, 입문]
tags: [C, 포인터, 메모리]
---

여기서부터 본문을 마크다운으로 작성합니다.
```

### 카테고리 규칙 (일관성 중요)

| 주제 | categories 예시 |
|---|---|
| C 언어 | `[C언어, 입문]` / `[C언어, 심화]` |
| C++ | `[C++, 입문]` |
| C# | `[C#, 입문]` |
| 컴퓨터과학 | `[컴퓨터과학, 입문]` |
| 알고리즘 | `[알고리즘, 입문]` |
| 게임기획 | `[게임기획, 입문]` |
| 유니티 | `[유니티, 입문]` |

### 코드 블록 작성법

````markdown
```c
#include <stdio.h>
int main() { return 0; }
```
````

지원 언어 키워드: `c`, `cpp`, `csharp`, `python`, `bash`, `yaml`, `markdown`

### 이미지 삽입

1. 이미지를 `assets/images/` 폴더에 저장
2. 마크다운에서 참조:
```markdown
![설명](../assets/images/파일명.png)
```

### 수식 (알고리즘 글에서 사용)

Front Matter에 `math: true` 추가 후:

```markdown
인라인: $O(n \log n)$
블록: $$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$
```

---

## 트러블슈팅

| 증상 | 해결 방법 |
|---|---|
| 빌드 실패 | 저장소 → Actions 탭에서 오류 메시지 확인 |
| 댓글이 안 보임 | Discussions 활성화 여부, repo_id/category_id 값 확인 |
| 글이 안 보임 | 파일명 날짜 형식 확인, date가 미래 날짜면 안 보임 |
| CSS가 안 적용됨 | `_config.yml`의 url이 정확한지 확인 |
| 로컬 서버 오류 | `bundle install` 재실행 |

---

## 참고 자료

- Chirpy 테마 공식 문서: https://chirpy.cotes.page/
- Giscus 공식 사이트: https://giscus.app/ko
- Jekyll 공식 문서: https://jekyllrb.com/docs/
- GitHub Pages 문서: https://docs.github.com/en/pages
