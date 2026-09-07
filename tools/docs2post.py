#!/usr/bin/env python3
"""Google Docs HTML 내보내기 → Chirpy 블로그 글 변환기.

Docs 문서는 사람이 읽고 검증하는 원본이다. 변환용 마커를 쓰지 않고
Docs의 기본 서식(제목 스타일, 표, 이미지, 등폭 글꼴)을 그대로 해석한다.

사용법:
    python tools/docs2post.py <내보낸.html> [-o _posts] [--check-only]

Docs 쪽 작성 규약은 기록/DOCS_AUTHORING.md 참고.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import io
import os
import re
import sys
from html.parser import HTMLParser

for _stream in (sys.stdout, sys.stderr):        # 윈도우 콘솔 한글 깨짐 방지
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

MONO_FONTS = ("roboto mono", "consolas", "courier", "monospace", "source code pro", "d2coding")

BOX_PREFIX = {           # Docs 문단 맨 앞에 쓰는 말 → Chirpy 알림 박스
    "참고:": "prompt-info",
    "팁:": "prompt-tip",
    "주의:": "prompt-warning",
    "금지:": "prompt-danger",
}

RESULT_LABEL = ("실행 결과", "실행결과", "출력 결과", "출력결과", "결과")

MERMAID_HEAD = ("flowchart", "graph ", "sequencediagram", "classdiagram",
                "statediagram", "erdiagram", "gantt", "pie ", "mindmap")

SHELL_HEAD = ("dotnet", "code ", "cd ", "git ", "npm ", "python ", "bundle ",
              "ls", "dir", "mkdir", "echo ", "curl ")

META_KEYS = {           # Docs 메타 표에서 쓰는 한국어 키 → front matter 키
    "제목": "title", "날짜": "date", "카테고리": "categories", "태그": "tags",
    "슬러그": "slug", "수식": "math", "다이어그램": "mermaid",
    "썸네일": "image", "썸네일 설명": "image_alt", "기본 언어": "deflang",
}

BANNED_SECTIONS = ["왜 배우는가", "직접 해보며 확인한 것", "궁금했던 점", "확인 방법"]


# ── 문서 모델 ──────────────────────────────────────────────────────────

class Run:
    __slots__ = ("text", "bold", "italic", "mono", "href")

    def __init__(self, text: str, bold=False, italic=False, mono=False, href=None):
        self.text, self.bold, self.italic, self.mono, self.href = text, bold, italic, mono, href


class Block:
    def __init__(self, kind: str, **kw) -> None:
        self.kind = kind                 # heading | para | li | table | image
        self.__dict__.update(kw)


class DocsHTML(HTMLParser):
    """Docs가 내보낸 HTML을 블록 목록으로 편다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.mono_classes: set[str] = set()
        self._style_buf: list[str] = []
        self._in_style = False
        self._stack: list[tuple[str, dict]] = []
        self._runs: list[Run] = []
        self._cur: str | None = None      # 현재 모으는 블록 종류
        self._level = 0
        self._list_depth = 0
        self._list_kind: list[str] = []
        self._table: list[list[list[Run]]] | None = None
        self._row: list[list[Run]] | None = None

    # 인라인 서식 상태 --------------------------------------------------
    def _fmt(self) -> tuple[bool, bool, bool, str | None]:
        bold = italic = mono = False
        href = None
        for tag, attrs in self._stack:
            if tag in ("b", "strong"):
                bold = True
            if tag in ("i", "em"):
                italic = True
            if tag == "a" and attrs.get("href"):
                href = attrs["href"]
            style = (attrs.get("style") or "").lower()
            if "font-weight:700" in style or "font-weight:bold" in style:
                bold = True
            if "font-style:italic" in style:
                italic = True
            if any(f in style for f in MONO_FONTS):
                mono = True
            for cls in (attrs.get("class") or "").split():
                if cls in self.mono_classes:
                    mono = True
        return bold, italic, mono, href

    # 파서 콜백 ---------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "style":
            self._in_style = True
            return
        if tag == "img":
            self.blocks.append(Block("image", src=a.get("src", ""), alt=a.get("alt", "")))
            return
        if tag == "br":
            self._runs.append(Run("\n"))
            return

        self._stack.append((tag, a))

        if re.fullmatch(r"h[1-6]", tag):
            self._flush()
            self._cur, self._level = "heading", int(tag[1])
        elif tag == "p":
            self._flush()
            self._cur = "para"
        elif tag in ("ul", "ol"):
            self._list_depth += 1
            self._list_kind.append(tag)
        elif tag == "li":
            self._flush()
            self._cur = "li"
        elif tag == "table":
            self._flush()
            self._table = []
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._flush()
            self._cur = "cell"

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False
            self._parse_style("".join(self._style_buf))
            return
        if tag in ("img", "br"):
            return

        if tag in ("td", "th") and self._row is not None:
            self._row.append(self._runs)
            self._runs, self._cur = [], None
        elif tag == "tr" and self._table is not None:
            if self._row:
                self._table.append(self._row)
            self._row = None
        elif tag == "table":
            if self._table:
                self.blocks.append(Block("table", rows=self._table))
            self._table = None
        elif tag in ("ul", "ol"):
            self._flush()
            self._list_depth = max(0, self._list_depth - 1)
            if self._list_kind:
                self._list_kind.pop()
        elif tag in ("p", "li") or re.fullmatch(r"h[1-6]", tag):
            self._flush()

        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._in_style:
            self._style_buf.append(data)
            return
        if not data or self._cur is None:
            return
        b, i, m, href = self._fmt()
        self._runs.append(Run(data, b, i, m, href))

    # 내부 --------------------------------------------------------------
    def _parse_style(self, css: str) -> None:
        for m in re.finditer(r"\.([\w-]+)\s*\{([^}]*)\}", css):
            if any(f in m.group(2).lower() for f in MONO_FONTS):
                self.mono_classes.add(m.group(1))

    def _flush(self) -> None:
        if self._cur is None:
            self._runs = []
            return
        if self._cur == "cell":
            return
        runs = self._runs
        self._runs = []
        if not "".join(r.text for r in runs).strip():
            self._cur = None
            return
        if self._cur == "heading":
            self.blocks.append(Block("heading", level=self._level, runs=runs))
        elif self._cur == "li":
            ordered = bool(self._list_kind) and self._list_kind[-1] == "ol"
            self.blocks.append(Block("li", depth=max(0, self._list_depth - 1),
                                     ordered=ordered, runs=runs))
        else:
            self.blocks.append(Block("para", runs=runs))
        self._cur = None


# ── 블록 → 마크다운 ────────────────────────────────────────────────────

def runs_text(runs: list[Run]) -> str:
    return "".join(r.text for r in runs)


def render_runs(runs: list[Run]) -> str:
    out = []
    for r in runs:
        t = r.text.replace(" ", " ")
        if not t:
            continue
        stripped = t.strip()
        if not stripped:
            out.append(t)
            continue
        lead = t[: len(t) - len(t.lstrip())]
        trail = t[len(t.rstrip()):]
        body = stripped
        if r.mono:
            body = f"`{body}`"
        if r.bold:
            body = f"**{body}**"
        if r.italic and not r.mono:
            body = f"_{body}_"
        if r.href:
            body = f"[{body}]({r.href})"
        out.append(lead + body + trail)
    return re.sub(r"[ \t]+", " ", "".join(out)).strip()


def all_mono(runs: list[Run]) -> bool:
    real = [r for r in runs if r.text.strip()]
    return bool(real) and all(r.mono for r in real)


def guess_lang(lines: list[str], prev_label: bool, default: str) -> str:
    head = (lines[0] if lines else "").strip().lower()
    if head.startswith(MERMAID_HEAD):
        return "mermaid"
    if prev_label:
        return "text"
    if all(l.strip().lower().startswith(SHELL_HEAD) for l in lines if l.strip()):
        return "bash"
    return default


class Doc:
    def __init__(self) -> None:
        self.meta: dict[str, str] = {}
        self.body: list[str] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []
        self.images: list[str] = []


def save_image(src: str, doc: Doc, repo_root: str, src_dir: str, index: int) -> str | None:
    slug = doc.meta.get("slug", "post")
    out_dir = os.path.join(repo_root, "assets", "img", "posts", slug)
    os.makedirs(out_dir, exist_ok=True)

    if src.startswith("data:"):
        m = re.match(r"data:image/(\w+);base64,(.*)", src, re.S)
        if not m:
            doc.errors.append(f"이미지 {index}: data URI를 해석할 수 없음")
            return None
        ext = {"jpeg": "jpg"}.get(m.group(1).lower(), m.group(1).lower())
        blob = base64.b64decode(m.group(2))
    else:                                     # 압축 해제한 내보내기의 images/ 상대 경로
        path = os.path.join(src_dir, src.replace("/", os.sep))
        if not os.path.exists(path):
            doc.errors.append(f"이미지 파일을 찾을 수 없음: {src}")
            return None
        ext = (os.path.splitext(path)[1] or ".png").lstrip(".").lower()
        blob = io.open(path, "rb").read()

    name = f"img-{index:02d}.{ext}"
    target = os.path.join(out_dir, name)
    digest = hashlib.sha1(blob).hexdigest()
    if os.path.exists(target):
        old = hashlib.sha1(io.open(target, "rb").read()).hexdigest()
        if old != digest:
            io.open(target, "wb").write(blob)
    else:
        io.open(target, "wb").write(blob)
    doc.images.append(name)
    return f"/assets/img/posts/{slug}/{name}"


def read_meta_table(rows, doc: Doc) -> bool:
    """첫 표가 메타 표면 읽어서 소비한다."""
    keys = [runs_text(r[0]).strip().rstrip(":") for r in rows if len(r) >= 2]
    if not keys or not any(k in META_KEYS or k.lower() in META_KEYS.values() for k in keys):
        return False
    for row in rows:
        if len(row) < 2:
            continue
        k = runs_text(row[0]).strip().rstrip(":")
        v = runs_text(row[1]).strip()
        key = META_KEYS.get(k, k.lower())
        if key:
            doc.meta[key] = v
    return True


def render_table(rows) -> list[str]:
    out = []
    for i, row in enumerate(rows):
        cells = [render_runs(c).replace("|", "\\|") or " " for c in row]
        out.append("| " + " | ".join(cells) + " |")
        if i == 0:
            out.append("| " + " | ".join("---" for _ in cells) + " |")
    out.append("")
    return out


def build_body(blocks: list[Block], doc: Doc, repo_root: str, src_dir: str) -> None:
    default_lang = doc.meta.get("deflang", "csharp")
    meta_done = False
    img_index = 0
    i = 0
    num = 1
    prev_label = False

    while i < len(blocks):
        b = blocks[i]

        if b.kind == "table":
            if not meta_done and read_meta_table(b.rows, doc):
                meta_done = True
                i += 1
                continue
            if len(b.rows[0]) > 4:
                doc.warnings.append("표 열이 5개 이상 — 모바일에서 가로 스크롤됨")
            doc.body += render_table(b.rows)
            i += 1
            continue

        if b.kind == "image":
            img_index += 1
            path = save_image(b.src, doc, repo_root, src_dir, img_index)
            if path:
                alt = b.alt.strip()
                if not alt:
                    doc.errors.append(f"이미지 {img_index}: 대체 텍스트가 비어 있음")
                    alt = ""
                line = f"![{alt}]({path})"
                if not path.lower().endswith(".svg"):
                    line += '{: width="700" }'
                doc.body.append(line)
                # 바로 다음 문단이 전부 기울임이면 캡션으로 붙인다
                nxt = blocks[i + 1] if i + 1 < len(blocks) else None
                if (nxt and nxt.kind == "para"
                        and all(r.italic for r in nxt.runs if r.text.strip())):
                    doc.body.append("_" + runs_text(nxt.runs).strip() + "_")
                    i += 1
                doc.body.append("")
            i += 1
            continue

        if b.kind == "heading":
            level = b.level + 1          # Docs 제목1 = 블로그 H2
            if level > 3:
                doc.warnings.append(f"H{level} 사용 — 가이드상 H3까지만 허용: {runs_text(b.runs)[:30]}")
            doc.body += ["", "#" * min(level, 6) + " " + render_runs(b.runs), ""]
            prev_label = False
            i += 1
            continue

        if b.kind == "li":
            marker = f"{num}. " if b.ordered else "- "
            doc.body.append("  " * b.depth + marker + render_runs(b.runs))
            num = num + 1 if b.ordered else 1
            if i + 1 >= len(blocks) or blocks[i + 1].kind != "li":
                doc.body.append("")
                num = 1
            i += 1
            continue

        # 문단 -----------------------------------------------------------
        text = runs_text(b.runs).strip()

        if all_mono(b.runs):                          # 등폭 문단 = 코드
            lines = []
            while i < len(blocks) and blocks[i].kind == "para" and all_mono(blocks[i].runs):
                lines.append(runs_text(blocks[i].runs).replace(" ", " ").rstrip())
                i += 1
            lang = guess_lang(lines, prev_label, default_lang)
            doc.body += [f"```{lang}", *lines, "```", ""]
            prev_label = False
            continue

        for prefix, cls in BOX_PREFIX.items():        # 참고: / 주의: / 팁: / 금지:
            if text.startswith(prefix):
                inner = render_runs(b.runs)
                inner = inner[len(prefix):].strip() if inner.startswith(prefix) else inner
                doc.body += [f"> {inner}", f"{{: .{cls} }}", ""]
                break
        else:
            doc.body += [render_runs(b.runs), ""]

        prev_label = text.rstrip(":").strip() in RESULT_LABEL
        i += 1


# ── front matter · 검사 ────────────────────────────────────────────────

def front_matter(doc: Doc) -> list[str]:
    m = doc.meta
    for key in ("title", "date", "categories", "slug"):
        if not m.get(key):
            doc.errors.append(f"메타 표에 {key} 없음")

    def as_list(key: str) -> str:
        vals = [v.strip() for v in re.split(r"[,·]", m.get(key, "")) if v.strip()]
        return "[" + ", ".join(vals) + "]"

    fm = ["---",
          f'title: "{m.get("title", "")}"',
          f'date: {m.get("date", "")}',
          f'categories: {as_list("categories")}',
          f'tags: {as_list("tags")}',
          f'math: {m.get("math", "false")}',
          f'mermaid: {m.get("mermaid", "false")}',
          "comments: true"]
    if m.get("image"):
        fm += ["image:",
               f'  path: /assets/img/posts/{m.get("slug", "")}/{m["image"]}',
               f'  alt: {m.get("image_alt", m.get("title", ""))}']
    fm.append("---")

    cats = [v.strip() for v in re.split(r"[,·]", m.get("categories", "")) if v.strip()]
    if len(cats) != 2:
        doc.warnings.append(f"categories가 2단계가 아님: {cats}")
    return fm


def validate(doc: Doc, body: str) -> None:
    if "## 학습 목표" not in body:
        doc.errors.append("`## 학습 목표` 섹션 없음 (Docs 제목1로 작성)")
    for banned in BANNED_SECTIONS:
        if re.search(rf"^#+\s*{re.escape(banned)}", body, re.M):
            doc.errors.append(f"금지된 섹션 사용: {banned}")

    goals = re.search(r"^## 학습 목표\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    if goals and "- [ ]" in goals.group(1):
        doc.errors.append("`학습 목표`에 체크박스 사용 — 일반 불릿으로")

    for lang in re.findall(r"^```(\w*)\s*$", body, re.M)[::2]:
        if not lang:
            doc.warnings.append("언어 태그 없는 코드 블록")

    if "```mermaid" in body and doc.meta.get("mermaid", "").lower() != "true":
        doc.errors.append("mermaid 다이어그램이 있는데 메타 표의 '다이어그램'이 true가 아님")

    if re.search(r"[“”‘’]", body):
        doc.warnings.append("스마트 따옴표 발견 — Docs 자동 대체 설정을 끌 것")


def build(text: str, repo_root: str, src_dir: str) -> tuple[Doc, str, str]:
    parser = DocsHTML()
    parser.feed(text)
    parser.close()

    doc = Doc()
    build_body(parser.blocks, doc, repo_root, src_dir)
    fm = front_matter(doc)

    lines: list[str] = []
    for line in doc.body:
        if not line.strip() and lines and not lines[-1].strip():
            continue
        lines.append(line.rstrip())
    body = "\n".join(lines).strip() + "\n"

    validate(doc, body)
    date = doc.meta.get("date", "")[:10]
    slug = doc.meta.get("slug", "post")
    return doc, f"{date}-{slug}.md", "\n".join(fm) + "\n\n" + body


def load_input(path: str) -> tuple[str, str]:
    """.html 파일 또는 Docs가 만든 .zip을 읽어 (HTML 텍스트, 이미지 기준 경로)를 준다."""
    if path.lower().endswith(".zip"):
        import tempfile, zipfile
        tmp = tempfile.mkdtemp(prefix="docs2post-")
        with zipfile.ZipFile(path) as z:
            z.extractall(tmp)
        for root, _, files in os.walk(tmp):
            for f in files:
                if f.lower().endswith((".html", ".htm")):
                    return io.open(os.path.join(root, f), encoding="utf-8").read(), root
        raise SystemExit("zip 안에 html 파일이 없습니다.")
    return io.open(path, encoding="utf-8").read(), os.path.dirname(os.path.abspath(path))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Docs에서 내보낸 .html 또는 .zip")
    ap.add_argument("-o", "--outdir", default="_posts")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text, src_dir = load_input(args.input)
    doc, name, out = build(text, repo_root, src_dir)

    for w in doc.warnings:
        print(f"[경고] {w}", file=sys.stderr)
    for e in doc.errors:
        print(f"[오류] {e}", file=sys.stderr)
    if doc.errors:
        print("\n오류가 있어 파일을 쓰지 않았습니다.", file=sys.stderr)
        return 1
    if args.check_only:
        print(f"검사 통과 (이미지 {len(doc.images)}장)")
        return 0

    path = os.path.join(args.outdir, name)
    io.open(path, "w", encoding="utf-8", newline="\n").write(out)
    print(f"작성됨: {path}  (이미지 {len(doc.images)}장)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
