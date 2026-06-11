# HANDOFF1 — giscus 댓글 미표시 문제 해결 기록

작성일: 2026-06-10
대상 저장소: `hyunwoonam-digipen/hyunwoonam-digipen.github.io` (Chirpy v7.5.0, GitHub Pages)

---

## 1. 증상

블로그 글 페이지 하단에 giscus 댓글창이 전혀 나타나지 않음.
GitHub Discussions 활성화, giscus 앱 설치, 저장소 권한 부여는 모두 정상 상태였음.

## 2. 근본 원인

`_config.yml`의 댓글 설정 키가 잘못됨.

- Chirpy **7.x**는 댓글 활성화 키로 `comments.provider`를 읽음.
- 설정에는 구버전(5~6.x) 문법인 `comments.active: giscus`가 들어 있었음.
- 그 결과 테마가 `site.comments.provider`를 빈 값으로 인식 → 댓글 include 자체를 건너뜀.

### 근거 (테마 소스 확인)

`_includes/comment.html` (Chirpy v7.5.0) 트리거 조건:

```liquid
{% if page.comments and site.comments.provider %}
  {% capture path %}comments/{{ site.comments.provider }}.html{% endcapture %}
  {% include {{ path }} %}
{% endif %}
```

- `page.comments` → 모든 글 front matter + `_config.yml` defaults에서 `true`. ✅ 충족
- `site.comments.provider` → 수정 전엔 빈 값(=비활성). ❌ → 댓글 미표시의 직접 원인

## 3. 수정 내용

파일: `_config.yml` (37번째 줄)

```diff
 comments:
-  active: giscus
+  provider: giscus   # Chirpy 7.x는 'active'가 아니라 'provider' 키를 사용
   giscus:
     repo: hyunwoonam-digipen/hyunwoonam-digipen.github.io
     repo_id: "R_kgDOSAnymQ"
     category: Comments
     category_id: "DIC_kwDOSAnymc4C6rnK"
     mapping: pathname
     input_position: bottom
     lang: ko
     reactions_enabled: "1"
```

giscus 하위 값(repo / repo_id / category / category_id 등)은 원래 정상이라 그대로 둠.

## 4. 커밋 / 배포 진행 과정

- 샌드박스에서 커밋 생성: `91bd2f7` ("fix: giscus 댓글 키를 active에서 provider로 변경")
- 샌드박스에서는 GitHub 인증 정보가 없어 **푸시 불가** → 사용자가 로컬 git GUI에서 푸시.
- 중간에 `.git/index.lock`, `HEAD.lock`, `objects/maintenance.lock` 잔여 파일로 GUI 스테이징/커밋 오류 발생.
  - 원인: 샌드박스 git 작업이 남긴 lock 파일을 마운트 권한 문제로 unlink 못 함.
  - 조치: lock 파일을 옆으로 옮겨(rename) 제거.
- 최종적으로 사용자가 푸시 완료.

### 배포 검증 (완료)

원격 `main`의 `_config.yml`을 직접 확인 → `provider: giscus` 반영 확인됨.

```
https://raw.githubusercontent.com/hyunwoonam-digipen/hyunwoonam-digipen.github.io/main/_config.yml
→ comments.provider: giscus  ✅
```

즉 **코드/설정상으로는 댓글이 표시되어야 하는 상태**.

## 5. 현재 상태 / 남은 확인 사항

수정과 배포는 끝났으나, 사용자 화면에 아직 댓글창이 안 보이는 단계.
남은 변수는 코드가 아니라 **배포 캐시 / 재빌드 타이밍 + giscus 런타임**으로 좁혀짐.

확인 순서:

1. **Pages 빌드 완료 확인** — GitHub 저장소 → Actions 탭 → "pages build and deployment" 초록 체크 (푸시 후 1~2분).
2. **강력 새로고침** — 글 페이지에서 `Ctrl + Shift + R`. (GitHub Pages·브라우저가 이전 HTML 캐싱)
3. **댓글 위치** — giscus는 페이지 맨 아래, "이전 글 / 다음 글" 박스 **아래**에 렌더됨.

### 만약 그래도 안 되면 (다음 디버깅 분기)

- 빈 칸이 아니라 **giscus 오류 박스**("discussion not found" 등)가 뜨면 → `repo_id`/`category_id` 불일치 신호.
  - https://giscus.app 에서 repo(`hyunwoonam-digipen/...`)·카테고리(`Comments`) 재입력 후 나오는 값과 현재 설정값 비교.
- 브라우저 콘솔(F12) giscus 오류 메시지 확보가 가장 확실 (현재 세션에선 연결된 브라우저가 없어 콘솔 확인 미수행).

## 6. 참고 사실 (작업 중 발견)

- 실제 글 URL이 Chirpy 기본형(`/posts/:title/`)이 아니라 카테고리 기반
  (예: `/유니티/입문/2025/04/07/unity-intro.html`).
  - `_config.yml` posts defaults에 `permalink: /posts/:title/`가 없어 Jekyll 기본 permalink가 적용된 것.
  - 댓글 동작에는 영향 없음(`mapping: pathname`이라 pathname 기준으로 매핑). 필요 시 별도 정리 항목.
- 미설정 placeholder: `analytics.goatcounter.id: GOATCOUNTER_CODE` (방문자 통계 미연동 상태). 댓글과 무관.

## 7. 미검증 / 리스크

- ~~`repo_id`(`R_kgDOSAnymQ`)·`category_id`(`DIC_kwDOSAnymc4C6rnK`)가 실제 저장소/카테고리와 일치하는지는 미검증.~~ → **검증 완료 (아래 8장)**
- 연결된 브라우저가 없어 giscus 런타임(콘솔) 직접 검증은 못 함. (브라우저 연결 시 추가 가능)

## 8. 추가 검증 (2026-06-11, HANDOFF 이어서)

### 8.1 원격 설정 재확인 ✅
- 로컬 `main` ↔ `origin/main` 동기화 상태, 미푸시 변경 없음.
- 이후 커밋(`aeb2a1f`, `8cf03f9`)에도 `comments.provider: giscus` 유지됨.
- 원격 raw `_config.yml`에서 `provider: giscus` + giscus 하위값 그대로 확인.

### 8.2 배포 페이지 정상 렌더 ✅
- 라이브 글(`/유니티/입문/.../unity-intro.html`) 정상 응답, 본문/네비/관련글 모두 렌더.
- 주의: web_fetch는 HTML→마크다운 변환 과정에서 `<script>`(giscus client.js)를 제거하므로,
  giscus `<script>` 태그 자체를 fetch 텍스트에서 직접 확인하는 것은 불가. (런타임 확인은 브라우저 필요)

### 8.3 giscus 노드 ID 내부 일관성 검증 ✅ (핵심)
msgpack 디코딩 결과:

- `repo_id`  `R_kgDOSAnymQ`        → `[0, 1208674457]`            → 저장소 DB id = **1208674457**
- `category_id` `DIC_kwDOSAnymc4C6rnK` → `[0, 1208674457, 48871370]` → 저장소 id **1208674457**(동일) + 카테고리 id 48871370

→ `category_id`가 `repo_id`와 **동일한 저장소 식별자**를 포함. 두 값이 서로 일치하며 같은 저장소를 가리킴이 확인됨.
   (잘못 붙여넣은 값/placeholder였다면 이 내부 일관성이 성립하지 않음.) → 리스크 7번 해소.

### 8.4 남은 단 하나 (런타임)
설정·배포·ID 정합성은 모두 통과. 코드/설정상 댓글이 표시되어야 하는 상태가 재확인됨.
유일한 미확인 항목은 **실제 브라우저에서의 giscus 런타임 렌더**:
- 글 페이지 `Ctrl+Shift+R` 강력 새로고침 후 맨 아래(이전/다음 글 박스 아래) 확인.
- 여전히 안 보이면 F12 콘솔의 giscus 메시지 확보 → 그때 추가 디버깅.
- 브라우저를 Claude에 연결하면 런타임 직접 검증 가능.
